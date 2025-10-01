
import pygame
import numpy as np
import random

class Infection:
    def __init__(self):
        # Screen & grid
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        # State grid: 0 = safe, 1 = infected
        self.state = np.zeros((self.height, self.width), dtype=np.uint8)  # (H, W)
        # Separate "dead" mask to keep same behavior as before (not drawn by default)
        self.dead = np.zeros_like(self.state, dtype=bool)

        # Seed infection at center
        cy, cx = self.height // 2, self.width // 2
        self.state[cy, cx] = 1

        # Timing/probas
        self.time_last_infection = 0
        self.dt_ms = 10
        self.contact_infect_p = 2 / 15.0   # per-neighbor prob (same ballpark as your loop)
        self.death_p = 1 / 15.0
        self.air_transmission_is_active = True
        self.air_event_chance = 1 / 100.0
        self.air_jump_radius = 400

        # Pre-allocate helpers
        self._rng = np.random.default_rng()

    # ===== Helpers for neighborhood logic (8-neighborhood via array rolls) =====
    def _neighbor_count(self, grid):
        # Sum infected neighbors from 8 directions using wrap=False style by padding with zeros.
        g = grid
        H, W = g.shape
        # Pad to avoid wrap-around when rolling
        pad = np.pad(g, pad_width=1, mode='constant', constant_values=0)

        # Extract shifted views (avoids multiple rolls)
        # Using slicing on the padded grid is faster and avoids wrap issues.
        n  = pad[0:H,   0:W]   # up-left
        ne = pad[0:H,   1:W+1] # up
        e  = pad[0:H,   2:W+2] # up-right
        w  = pad[1:H+1, 0:W]   # left
        c  = pad[1:H+1, 1:W+1] # center (unused directly)
        er = pad[1:H+1, 2:W+2] # right
        sw = pad[2:H+2, 0:W]   # down-left
        se = pad[2:H+2, 1:W+1] # down
        s  = pad[2:H+2, 2:W+2] # down-right

        # Sum all except center
        return (n + ne + e + w + er + sw + se + s)

    # ===== Transmission rules =====
    def contact_transmission(self):
        # Compute number of infected neighbors for every pixel
        infected = (self.state == 1)
        neigh = self._neighbor_count(infected.astype(np.uint8))

        # Candidates: safe & not dead & has ≥1 infected neighbor
        candidates = (self.state == 0) & (~self.dead) & (neigh > 0)

        if not np.any(candidates):
            return

        # For each candidate with n neighbors, infection probability = 1 - (1-p)^n
        # Draw uniform randoms and infect where rand < prob
        n = neigh[candidates].astype(np.float32)
        p = 1.0 - (1.0 - self.contact_infect_p) ** n

        r = self._rng.random(p.shape, dtype=np.float32)
        will_infect = (r < p)

        # Apply
        idxs = np.argwhere(candidates)
        if idxs.size:
            chosen = idxs[will_infect]
            if chosen.size:
                self.state[chosen[:, 0], chosen[:, 1]] = 1

    def air_transmission(self):
        if not self.air_transmission_is_active:
            return

        if self._rng.random() < self.air_event_chance:
            infected_positions = np.argwhere((self.state == 1) & (~self.dead))
            if infected_positions.size == 0:
                return

            # Pick a random infected "reference" then jump within a radius box
            ref_y, ref_x = infected_positions[self._rng.integers(0, len(infected_positions))]
            # Retry a few times to land somewhere valid
            for _ in range(16):
                dy = self._rng.integers(-self.air_jump_radius, self.air_jump_radius + 1)
                dx = self._rng.integers(-self.air_jump_radius, self.air_jump_radius + 1)
                ny, nx = ref_y + dy, ref_x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if (self.state[ny, nx] == 0) and (not self.dead[ny, nx]):
                        self.state[ny, nx] = 1
                        break

    def update_infected_number(self):
        self.contact_transmission()
        self.air_transmission()

    def update_dead_number(self):
        infected = (self.state == 1) & (~self.dead)
        if not np.any(infected):
            return
        # Randomly kill some infected
        kill_draw = self._rng.random(infected.shape, dtype=np.float32)
        will_die = infected & (kill_draw < self.death_p)
        if np.any(will_die):
            self.dead[will_die] = True
            self.state[will_die] = 0  # remove from infected

    def update_infection(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_infection >= self.dt_ms:
            self.time_last_infection = current_time
            self.update_infected_number()
            self.update_dead_number()

    # ===== Rendering =====
    def draw(self, surf):
        # Fast blit using surfarray; white background, red for infected, optional gray for dead.
        H, W = self.state.shape
        # Start with white
        rgb = np.full((H, W, 3), 255, dtype=np.uint8)

        infected = (self.state == 1)
        # Red for infected
        rgb[infected] = (255, 0, 0)

        # Uncomment if you want to show "dead" pixels in gray:
        # rgb[self.dead] = (128, 128, 128)

        # Pygame expects (W, H, 3) for blit_array with 24-bit surfaces
        pygame.surfarray.blit_array(surf, np.transpose(rgb, (1, 0, 2)))

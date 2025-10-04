
import pygame
import numpy as np
import random

class Infection:
    def __init__(self):
        # Screen and grid
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        # State_grid : 0 = safe, 1 = infected, 2 = dead
        self.state_grid = np.zeros((self.height, self.width), dtype=np.uint8)
        # Separate "dead" mask to keep same behavior as before (not drawn by default)
        self.dead = np.zeros_like(self.state_grid, dtype=bool)

        # Premier pixel infecté au centre
        y, x = self.height // 2, self.width // 2
        self.state_grid[y, x] = 1

        # Timing et probabilitées
        self.time_last_infection = 0
        self.time_between_infections = 10 # ms
        self.contact_infect_probability = 2 / 15
        self.air_transmission_is_active = True
        self.air_infect_probability = 1 / 100
        self.air_jump_radius = 400
        self.death_probability = 1 / 15

        # On cree un generateur d'aleatoire avec numpy
        self.rng = np.random.default_rng()

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
        infected = (self.state_grid == 1)
        neigh = self._neighbor_count(infected.astype(np.uint8))

        # Candidates: safe & not dead & has ≥1 infected neighbor
        candidates = (self.state_grid == 0) & (~self.dead) & (neigh > 0)

        if not np.any(candidates):
            return

        # For each candidate with n neighbors, infection probability = 1 - (1-p)^n
        # Draw uniform randoms and infect where rand < prob
        n = neigh[candidates].astype(np.float32)
        p = 1.0 - (1.0 - self.contact_infect_probability) ** n

        r = self.rng.random(p.shape, dtype=np.float32)
        will_infect = (r < p)

        # Apply
        idxs = np.argwhere(candidates)
        if idxs.size:
            chosen = idxs[will_infect]
            if chosen.size:
                self.state_grid[chosen[:, 0], chosen[:, 1]] = 1

    def air_transmission(self):
        if not self.air_transmission_is_active:
            return

        if self.rng.random() < self.air_infect_probability:
            infected_positions = np.argwhere((self.state_grid == 1) & (~self.dead))
            if infected_positions.size == 0:
                return

            # Pick a random infected "reference" then jump within a radius box
            ref_y, ref_x = infected_positions[self.rng.integers(0, len(infected_positions))]
            # Retry a few times to land somewhere valid
            for _ in range(16):
                dy = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1)
                dx = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1)
                ny, nx = ref_y + dy, ref_x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if (self.state_grid[ny, nx] == 0) and (not self.dead[ny, nx]):
                        self.state_grid[ny, nx] = 1
                        break

    def update_infected_number(self):
        self.contact_transmission()
        self.air_transmission()


    def update_dead_number(self) :
        infected_px_coords = np.column_stack(np.where(self.state_grid == 1)) # stockage des coords infectés -> sous forme [(x, y), (x, y)...]
        # Si aucun pixel infecté on arrete la fonction
        if not np.any(infected_px_coords) :
            return
        
        # On tue aleatoirement certains pixels infectés
        random_selection = self.rng.integers(0, 16, size=len(infected_px_coords), dtype=np.uint8) # on donne a chaque position de pixel infecté un nombre aleatoire stocké dans le tableau random_selection
        px_to_kill = infected_px_coords[(random_selection == 1)] # on stock dans le tableau px_to_kill les positions des pixels infectés qui ont eu le nombre 1 et qui vont donc mourir -> sous forme [(x, y), (x, y)...]
        
        x, y = np.transpose(px_to_kill) # on est obliger grace a np.transpose de redecouper [(x, y), (x, y)...] en deux tableau [x, x, x...], [y, y, y...] car c'est comme ca que numpy geres les positions (a l'etape d'apres)
        self.state_grid[x, y] = 2  # on passe la valeur des pixels morts a 2 dans le tableau numpy qui stock l'etat de chaque pixel


    def update_infection(self) :
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_infection >= self.time_between_infections:
            self.time_last_infection = current_time
            self.update_infected_number()
            self.update_dead_number()


    # ===== AFFICHAGE =====
    def draw(self, screen):
        # Blanc pour les pixels
        rgb = np.full((self.height, self.width, 3), (255, 255, 255), dtype=np.uint8)

        # Rouge pour les infectés
        infected = (self.state_grid == 1)
        rgb[infected] = (255, 0, 0)
        
        # Gris pour les pixels morts
        dead = (self.state_grid == 2)
        rgb[dead] = (128, 128, 128)

        # np.transpose parce que tableau numpy -> hauteur, largeur et fenetre pygame -> largeur, hauteur
        color_grid = np.transpose(rgb, (1, 0, 2))
        pygame.surfarray.blit_array(screen, color_grid)

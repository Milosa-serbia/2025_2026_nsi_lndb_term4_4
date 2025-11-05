import pygame
import numpy as np
import random

class Infection:
    def __init__(self):
        # Screen et grid
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        # State_grid : 0 = safe, 1 = infected, 2 = dead
        self.state_grid = np.load('dessin.npy')
        # Separate "dead" mask to keep same behavior as before (not drawn by default)
        self.dead = np.zeros_like(self.state_grid, dtype=bool)

        # Premier pixel infecté au centre
        y, x = self.height // 2, self.width // 2
        self.state_grid[y, x] = 1

        # Timing et probabilitées
        self.time_last_infection = 0
        self.time_between_infections = 10 # ms
        self.contact_infect_probability = 8 / 15
        self.air_transmission_is_active = True
        self.air_infect_probability = 1 / 1
        self.air_jump_radius = 300
        self.death_probability = 1 / 15

        self.invalid_statue_for_contamination = [1, 2] # le statut des pixels invalides pour la containation (donc deja mort, deja infectes...)

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
        if self.air_transmission_is_active :

            if self.rng.random(dtype=np.float32) < self.air_infect_probability :
                infected_positions = np.argwhere(self.state_grid == 1) # les pixels deja infectés (servent de reference pour la contamination par air) -> sous la forme [(y, x), (y, x)...]
                
                if np.any(infected_positions) :
                    # On choisi aleatoirement un pixel infecté qui servira de reference pour la contamination par air (centre du rayon de contamination) -> coordonnées renvoyées sous forme y, x
                    infected_ref_y, infected_ref_x = infected_positions[self.rng.integers(0, len(infected_positions))]
                    
                    # Si la 1ere contamination n'a pas marche on en refait une (jusqu'a 16 essais)
                    for _ in range(16):
                        additional_y = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1) # distance sur l'axe des ordonnées du pixel infecté de reference
                        additional_x = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1) # distance sur l'axe des abscisses du pixel infecté de reference
                        air_contamination_y, air_contamination_x = infected_ref_y + additional_y, infected_ref_x + additional_x # calcul de la position du nouveau foyer de contamination -> coordonnées renvoyées sous forme y, x
                        if (0 <= air_contamination_y < self.height) and (0 <= air_contamination_x < self.width) : # on verifie que le nouveau foyer n'apparaisse pas hors de la fenetre
                            if self.state_grid[air_contamination_y, air_contamination_x] not in self.invalid_statue_for_contamination : 
                                self.state_grid[air_contamination_y, air_contamination_x] = 1
                                break


    def update_infected_number(self):
        self.contact_transmission()
        self.air_transmission()


    def update_dead_number(self) :
        infected_px_coords = np.argwhere(self.state_grid == 1) # stockage des coords infectés -> sous forme [(y, x), (y, x)...]
        # Si aucun pixel infecté on arrete la fonction
        
        if np.any(infected_px_coords) :
            # On tue aleatoirement certains pixels infectés
            random_selection = self.rng.random(size=len(infected_px_coords), dtype=np.float32) # on donne a chaque position de pixel infecté un nombre aleatoire entre 0 et 1 stocké dans le tableau random_selection
            px_to_kill = infected_px_coords[(random_selection < self.death_probability)] # on stock dans le tableau px_to_kill les positions des pixels infectés qui ont eu un nombre inferieur a la proba de mort -> sous forme [(y, x), (y, x)...]
            
            ys, xs = np.transpose(px_to_kill) # on est obliger grace a np.transpose de redecouper [(y, x), (y, x)...] en deux tableau [y, y, y...], [x, x, x...] car c'est comme ca que numpy geres les positions (a l'etape d'apres)
            self.state_grid[ys, xs] = 2  # on passe la valeur des pixels morts a 2 dans le tableau numpy qui stock l'etat de chaque pixel


    def update_infection(self) :
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_infection >= self.time_between_infections :
            self.time_last_infection = current_time
            self.update_infected_number()
            self.update_dead_number()


    # ----- AFFICHAGE -----
    def draw(self, screen) :
        # Blanc pour les pixels
        rgb = np.full((self.height, self.width, 3), (255, 255, 255), dtype=np.uint8)

        # NIGGER pour les frontieres
        border = (self.state_grid == 255)
        rgb[border] = (0, 0, 0)

        # Rouge pour les infectés
        infected = (self.state_grid == 1)
        rgb[infected] = (255, 0, 0)
        
        # Gris pour les pixels morts
        dead = (self.state_grid == 2)
        rgb[dead] = (128, 128, 128)

        # np.transpose parce que tableau numpy -> hauteur, largeur et fenetre pygame -> largeur, hauteur
        color_grid = np.transpose(rgb, (1, 0, 2))
        pygame.surfarray.blit_array(screen, color_grid)

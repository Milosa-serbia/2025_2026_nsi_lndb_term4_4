import pygame
import numpy as np
import random
from brbr_data import *

class Infection :
    def __init__(self) :
        # Screen et grid
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()

        # Timing et probabilitées
        self.time_last_infection = 0
        self.time_between_infections = 100 # ms
        self.contact_infect_probability = 2 / 15
        self.air_transmission_is_active = True
        self.air_infect_probability = 1 / 100
        self.air_jump_radius = 300
        self.death_probability = 1 / 15

        # le statut des pixels invalides pour la containation (mer, deja mort, deja infectes...)
        self.invalid_statues_for_contamination = [1, 2, 100, 255] 

        # On cree un generateur d'aleatoire avec numpy
        self.rng = np.random.default_rng()
        
        # ---------------- PALETTE DE COULEUR ----------------
        self.palette = np.zeros((256, 3), dtype=np.uint8)

        # Couleurs fixes
        self.palette[255] = (0, 0, 0)            # frontières 
        self.palette[100] = (135, 206, 235)      # mer 
        self.palette[1]   = (255, 0, 0)          # infectés 
        self.palette[2]   = (135, 135, 135)      # morts 
        self.palette[101:148] = (250, 235, 140)
        # -------------------------------------------------------


    # ===== Voisins des pixels infectés pouvant etre infecté =====
    def neighbor_count(self, infected_positions, status_grid) :
        """
        Renvoie une liste [(y, x), ...] des candidats, doublons conservés.
        Règles:
        - voisin direct ajouté si valeur NOT IN invalid_statues_for_contamination
        - si voisin == 255 et direction cardinale (haut/bas/gauche/droite),
            on saute de 5 px dans la même direction; cible ajoutée si NOT IN invalid_statues_for_contamination
        """
        if infected_positions is None or len(infected_positions) == 0 :
            return []

        ys = infected_positions[:, 0] # stockage de tous les y des infected_positions -> sous forme [y, y, y...] (tableau 1D)
        xs = infected_positions[:, 1] # stockage de tous les x des infected_positions -> sous forme [x, x, x...] (tableau 1D)

        # 8 directions (dy, dx)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    ( 0, -1),           ( 0, 1),
                    ( 1, -1), ( 1, 0),  ( 1, 1)]

        candidates_ys = [] # y de tous les candidats vont etre stockés
        candidates_xs = [] # x de tous les candidats vont etre stockés

        invalid_statues = np.array(self.invalid_statues_for_contamination, dtype=np.uint8)

        for dy, dx in directions :
            # 1) voisins directs "safe" -> candidats
            neigh_ys = ys + dy # on rajoute dy a chaque elements de ys par ex [20, 28, 32] -> [21, 29, 33]
            neigh_xs = xs + dx # on rajoute dx a chaque elements de xs par ex [20, 28, 32] -> [21, 29, 33]

            neighbors_values = status_grid[neigh_ys, neigh_xs] # stockage de toutes les valeurs dans status_grid des voisins des infectés -> [status_grid[neigh_ys[0], neigh_xs[0]], status_grid[neigh_ys[1], neigh_xs[1]]...]

            safe_neighbors_values = ~np.isin(neighbors_values, invalid_statues) # on donne a chaque valeures de neighbors_values le bool True si elle n'est PAS dans invalid_statues -> sous forme [True, False, True...]
            candidates_ys.append(neigh_ys[safe_neighbors_values]) # stockage des y des neighbors_values qui sont safe -> sous forme [y, y, y...]
            candidates_xs.append(neigh_xs[safe_neighbors_values]) # stockage des x des neighbors_values qui sont safe -> sous forme [x, x, x...]

            # 2) saut au-dessus d'un border (255) uniquement haut, bas, gauche, droite (pour eviter une propagation trop rapide en diagonale)
            if (dy == 0) or (dx == 0) :  # True si haut, bas, gauche, droite
                border = (neighbors_values == 255)
                if np.any(border) :
                    # meme fonctionnement que le debut de la fonction mais les voisins sont a 5px de distance (saut des frontieres)
                    neigh_ys = (ys[border] + 5 * dy)
                    neigh_xs = (xs[border] + 5 * dx)

                    neighbors_values = status_grid[neigh_ys, neigh_xs]
                    
                    safe_neighbors_values = ~np.isin(neighbors_values, invalid_statues)
                    candidates_ys.append(neigh_ys[safe_neighbors_values])
                    candidates_xs.append(neigh_xs[safe_neighbors_values])

        if not candidates_ys :
            return []

        cy = np.concatenate(candidates_ys).astype(np.int32, copy=False)
        cx = np.concatenate(candidates_xs).astype(np.int32, copy=False)

        # On conserve les doublons
        return list(map(tuple, np.stack((cy, cx), axis=1)))


    # ===== Transmission par contact =====
    def contact_transmission(self, status_grid) :
        # Compute number of infected neighbors for every pixel
        infected_positions = np.argwhere(status_grid == 1) # stockage des coords infectés -> sous forme [(y, x), (y, x)...]
        neighbors_candidates = self.neighbor_count(infected_positions, status_grid) # On stock dans une liste les positions des voisins des infectés candidats a l'infection en cours : deja infectés ou morts -> sous forme [(y, x), (y, x)...]
        neighbors_candidates = np.asarray(neighbors_candidates, dtype=np.int32) # On transforme notre liste en object numpy -> sous forme [(y, x), (y, x)...]

        if np.any(neighbors_candidates):
            random_selection = self.rng.random(size=len(neighbors_candidates), dtype=np.float32) # on donne a chaque position de pixel candidat a l'infection un nombre aleatoire entre 0 et 1 stocké dans le tableau random_selection
            px_to_infect = neighbors_candidates[(random_selection < self.contact_infect_probability)] # on stock dans le tableau px_to_infect les positions des pixels candidats a l'infection qui ont eu un nombre inferieur a la proba d'infection par contact -> sous forme [(y, x), (y, x)...]
            
            ys, xs = np.transpose(px_to_infect) # on est obliger grace a np.transpose de redecouper [(y, x), (y, x)...] en deux tableau [y, y, y...], [x, x, x...] car c'est comme ca que numpy geres les positions (a l'etape d'apres)
            status_grid[ys, xs] = 1  # on passe la valeur des pixels infectés a 1 dans le tableau numpy qui stock l'etat de chaque pixel


    # ===== Transmission par air =====
    def air_transmission(self, status_grid) :
        if self.air_transmission_is_active :

            if self.rng.random(dtype=np.float32) < self.air_infect_probability :
                infected_positions = np.argwhere(status_grid == 1) # les pixels deja infectés (servent de reference pour la contamination par air) -> sous la forme [(y, x), (y, x)...]
                
                if np.any(infected_positions) :
                    # On choisi aleatoirement un pixel infecté qui servira de reference pour la contamination par air (centre du rayon de contamination) -> coordonnées renvoyées sous forme y, x
                    infected_ref_y, infected_ref_x = infected_positions[self.rng.integers(0, len(infected_positions))]
                    
                    # Si la 1ere contamination n'a pas marche on en refait une (jusqu'a 16 essais)
                    for _ in range(16) :
                        additional_y = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1) # distance sur l'axe des ordonnées du pixel infecté de reference
                        additional_x = self.rng.integers(-self.air_jump_radius, self.air_jump_radius + 1) # distance sur l'axe des abscisses du pixel infecté de reference
                        air_contamination_y, air_contamination_x = infected_ref_y + additional_y, infected_ref_x + additional_x # calcul de la position du nouveau foyer de contamination -> coordonnées renvoyées sous forme y, x
                        if (0 <= air_contamination_y < self.height) and (0 <= air_contamination_x < self.width) : # on verifie que le nouveau foyer n'apparaisse pas hors de la fenetre
                            if status_grid[air_contamination_y, air_contamination_x] not in self.invalid_statues_for_contamination : 
                                status_grid[air_contamination_y, air_contamination_x] = 1
                                break


    # ===== Mise a jour des mort / infectés =====
    def update_infected_number(self, status_grid) :
        self.contact_transmission(status_grid)
        self.air_transmission(status_grid)


    def update_dead_number(self, status_grid) :
        infected_px_coords = np.argwhere(status_grid == 1) # stockage des coords infectés -> sous forme [(y, x), (y, x)...]
        # Si aucun pixel infecté on arrete la fonction
        
        if np.any(infected_px_coords) :
            # On tue aleatoirement certains pixels infectés
            random_selection = self.rng.random(size=len(infected_px_coords), dtype=np.float32) # on donne a chaque position de pixel infecté un nombre aleatoire entre 0 et 1 stocké dans le tableau random_selection
            px_to_kill = infected_px_coords[(random_selection < self.death_probability)] # on stock dans le tableau px_to_kill les positions des pixels infectés qui ont eu un nombre inferieur a la proba de mort -> sous forme [(y, x), (y, x)...]
            
            ys, xs = np.transpose(px_to_kill) # on est obliger grace a np.transpose de redecouper [(y, x), (y, x)...] en deux tableau [y, y, y...], [x, x, x...] car c'est comme ca que numpy geres les positions (a l'etape d'apres)
            status_grid[ys, xs] = 2  # on passe la valeur des pixels morts a 2 dans le tableau numpy qui stock l'etat de chaque pixel
        

    def update(self, status_grid) :
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_infection >= self.time_between_infections :
            self.time_last_infection = current_time
            self.update_infected_number(status_grid)
            self.update_dead_number(status_grid)


    # ===== AFFICHAGE =====
    def draw(self, screen, state_grid, status_grid, menu_open) :
        rgb = self.palette[status_grid].copy()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if not menu_open :
            state_id = state_grid[mouse_y, mouse_x]
            if 101 <= state_id <= 147 :
                rgb[state_grid == state_id] = (rgb[state_grid == state_id] * 0.8).astype(np.uint8)
        rgb = np.transpose(rgb, (1, 0, 2))     
        pygame.surfarray.blit_array(screen, rgb)



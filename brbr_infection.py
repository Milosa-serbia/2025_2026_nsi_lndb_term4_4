import pygame
import numpy as np
import random

class Infection:
    def __init__(self):
        # Screen et grid
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        # State_grid : 0 = safe, 1 = infected, 2 = dead, 255 = border
        self.state_grid = np.load('dessin.npy')

        # Premier pixel infecté au centre
        y, x = self.height // 2, self.width // 2
        self.state_grid[y, x] = 1

        # Timing et probabilitées
        self.time_last_infection = 0
        self.time_between_infections = 10 # ms
        self.contact_infect_probability = 2 / 15
        self.air_transmission_is_active = True
        self.air_infect_probability = 1 / 100
        self.air_jump_radius = 300
        self.death_probability = 1 / 15

        # le statut des pixels invalides pour la containation (mer, deja mort, deja infectes...)
        self.invalid_statue_for_contamination = [1, 2, 100, 255] 

        # On cree un generateur d'aleatoire avec numpy
        self.rng = np.random.default_rng()
        
        # ---------------- PALETTE DE COULEUR ----------------
        self.palette = np.zeros((256, 3), dtype=np.uint8)

        # Couleurs fixes
        self.palette[255] = (0, 0, 0)            # frontières 
        self.palette[100] = (135, 206, 235)      # mer 
        self.palette[1]   = (255, 0, 0)          # infectés 
        self.palette[2]   = (120, 120, 120)      # morts 

        # ------- Dégradé jaune pour population 101 → 147 -------
        start = np.array([225, 210, 100], dtype=np.float32)    # jaune foncé mais pas trop
        end   = np.array([255, 255, 175], dtype=np.float32)    # jaune clair mais pas blanc
        steps = 147 - 101 + 1

        gradient = start + (np.linspace(0, 1, steps)[:, None] * (end - start))
        gradient = gradient.astype(np.uint8)

        self.palette[101:148] = gradient
        # -------------------------------------------------------


    # ===== Voisins des pixels infectés pouvant etre infecté =====
    def neighbor_count(self, infected_positions) :
        """
        À partir d'une liste de positions infectées [(y, x), ...],
        renvoie la liste des cases candidates à infecter :
        - les 8 voisins autour des infectés
        - si un voisin est un border (255), saute par-dessus (distance 2)
        """
        neighbors_candidates = []

        # Directions autour d'un px infecté
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1),
        ]

        for y, x in infected_positions :
            for add_y, add_x in directions :
                new_y, new_x = y + add_y, x + add_x
                
                if self.state_grid[new_y, new_x] not in self.invalid_statue_for_contamination : # si le px est safe alors il est candidats a l'infection
                    neighbors_candidates.append((new_y, new_x))

                elif self.state_grid[new_y, new_x] == 255 : # # si le px est une frontiere (sa position pointe sur 255 dans state_grid) alors on le saute et les pixels safe derriere lui sont candidats a l'infection
                    # tentative de "saut" par-dessus le border
                    if new_x == x :
                        new_y = y + 5 * add_y
                        if self.state_grid[new_y, new_x] not in self.invalid_statue_for_contamination :
                            neighbors_candidates.append((new_y, new_x))
                    if new_y == y :
                        new_x = x + 5 * add_x
                        if self.state_grid[new_y, new_x] not in self.invalid_statue_for_contamination :
                            neighbors_candidates.append((new_y, new_x))
                    
        return neighbors_candidates

            
    # ===== Transmission par contact =====
    def contact_transmission(self) :
        # Compute number of infected neighbors for every pixel
        infected_positions = np.argwhere(self.state_grid == 1) # stockage des coords infectés -> sous forme [(y, x), (y, x)...]
        neighbors_candidates = self.neighbor_count(infected_positions) # On stock dans une liste les positions des voisins des infectés candidats a l'infection en cours : deja infectés ou morts -> sous forme [(y, x), (y, x)...]
        neighbors_candidates = np.asarray(neighbors_candidates, dtype=np.int32) # On transforme notre liste en object numpy -> sous forme [(y, x), (y, x)...]

        if np.any(neighbors_candidates):
            random_selection = self.rng.random(size=len(neighbors_candidates), dtype=np.float32) # on donne a chaque position de pixel candidat a l'infection un nombre aleatoire entre 0 et 1 stocké dans le tableau random_selection
            px_to_infect = neighbors_candidates[(random_selection < self.contact_infect_probability)] # on stock dans le tableau px_to_infect les positions des pixels candidats a l'infection qui ont eu un nombre inferieur a la proba d'infection par contact -> sous forme [(y, x), (y, x)...]
            
            ys, xs = np.transpose(px_to_infect) # on est obliger grace a np.transpose de redecouper [(y, x), (y, x)...] en deux tableau [y, y, y...], [x, x, x...] car c'est comme ca que numpy geres les positions (a l'etape d'apres)
            self.state_grid[ys, xs] = 1  # on passe la valeur des pixels infectés a 1 dans le tableau numpy qui stock l'etat de chaque pixel


    # ===== Transmission par air =====
    def air_transmission(self) :
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


    # ===== Mise a jour des mort / infectés =====
    def update_infected_number(self) :
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


    # ===== AFFICHAGE =====
    def draw(self, screen) :
        rgb = self.palette[self.state_grid]   
        rgb = np.transpose(rgb, (1, 0, 2))     
        pygame.surfarray.blit_array(screen, rgb)



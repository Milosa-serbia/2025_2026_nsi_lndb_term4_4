import pygame
from brbr_infection import *
from brbr_ui import *

class Continent :
    def __init__(self) :
        # Initialisation infos fenetre
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Status_grid : 0 = safe, 1 = infected, 2 = dead, 255 = border , 100 = sea, 101:146 = states
        self.status_grid = np.load('dessin.npy')
        self.state_grid = self.status_grid.copy()
        
        # progression du vaccin
        self.vaccine_progression = 0
        
        # Temps entre les updates des infos et de l'infection
        self.time_last_update = 0
        self.time_between_updates = 10 # ms
        
        # Premier pixel infecté au centre
        self.status_grid[self.height // 2, self.width // 2] = 1
        
        # Infos des états
        self.infos = {}
        for id in STATES.keys() :
            self.infos[id] = KinderState( \
                STATES[id]['ui_pos'], \
                STATES[id]['name'], \
                STATES[id]['population'], \
                round(STATES[id]['population'] / len(np.argwhere(self.state_grid == id)), 5), \
                STATES[id]['vegetable_production'], \
                STATES[id]['obesity_rate'], \
                STATES[id]['importations'], \
                STATES[id]['exportations'] \
                    )
            
        self.lockdowned_state = []
        self.close_border_state = []
        
        # Instance de l'infection et de l'UI
        self.infection = Infection()
        self.ui = UI(self.infos, self.close_border_state, self.lockdowned_state)


    def handle_input(self, events) :
        x, y = pygame.mouse.get_pos()
        
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                # si le menu n'est pas ouvert
                if not self.ui.menu_open :
                    self.ui.px_id = self.state_grid[int(y), int(x)]
                    if self.ui.px_id not in self.infection.invalid_statues_for_contamination :   
                        self.ui.menu_open = True
                    
                # si le menu est ouvert        
                else :
                    if self.ui.menu2_open : # menu 1 et 2 ouverts
                        if not self.ui.menu2_rect.collidepoint(x, y) :
                            if not self.ui.menu_rect.collidepoint(x, y) :
                                self.ui.menu2_open = False
                                self.ui.menu_open = False
                            else :
                                self.ui.menu2_open = False
                    else : # uniquement menu 1 ouvert
                        if not self.ui.menu_rect.collidepoint(x, y) :
                            self.ui.menu_open = False
                    
    
    def update_infos(self) :
        flat = self.status_grid.ravel()
        counts = np.bincount(flat, minlength=256)

        # ===== 1) Mise à jour interne de chaque état (population, prod, stock) =====
        for id, state in self.infos.items() :  # pour tous les états
            # population vivante
            state.alive_population = counts[id] * state.population_per_px

            # production de base
            base_production = (
                state.initial_vegetable_production / state.population
            ) * state.alive_population

            # multiplicateur de prod :
            # - 1/3 si confinement
            # - 1/3 si frontières fermées
            factor = 1
            if state.lockdown :
                factor -= 1 / 3
            if state.closed_border :
                factor -= 1 / 3

            state.vegetable_production = base_production * factor

            # mise à jour du stock de nourriture (prod - conso)
            state.food_ressources += state.vegetable_production - (
                state.alive_population * (1 + state.obesity_rate)
            )

            # on empêche les réserves de tomber en dessous de 0
            if state.food_ressources < 0 :
                state.food_ressources = 0

        # ===== 2) Gestion des exportations =====
        for id, state in self.infos.items() :
            # pour chaque couple [id_destination, pourcentage]
            for export_id, export_part in state.exportations :
                # si l'id est 0 alors pas d'export defini
                if export_id == 0 or export_part <= 0 :
                    continue

                dest = self.infos[export_id]

                # quantité que l'état voudrait exporter pendant ce update
                wanted = state.vegetable_production * export_part
                if wanted <= 0 :
                    continue

                # on ne peut pas exporter plus que ce qu'on a en stock
                available = state.food_ressources
                if available <= 0 :
                    break  # plus rien à exporter pour cet état

                sent = min(wanted, available)

                # on retire du stock de l'exportateur
                state.food_ressources -= sent
                # on ajoute au stock du destinataire
                dest.food_ressources += sent

        # ===== 3) sécurité finale =====
        for state in self.infos.values() :
            if state.food_ressources < 0 :
                state.food_ressources = 0


    def update_and_draw(self, events) :
        if self.vaccine_progression < 100 :
            self.vaccine_progression += 0.125
            prev_menu_open = self.ui.menu_open
            self.handle_input(events) # on gere les input hors menu
            if self.ui.menu_open and prev_menu_open :
                self.ui.handle_input(events) # on gere les input dans les menu
            current_time = pygame.time.get_ticks()
            if current_time - self.time_last_update >= self.time_between_updates : # on fait une update de l'infection et des etats a intervals de temps reguliers
                self.time_last_update = current_time
                self.infection.update(self.status_grid, self.close_border_state, self.lockdowned_state) # update de l'infection
                self.update_infos() # update des infos des etats
            self.infection.draw(self.screen, self.state_grid, self.status_grid, self.ui.menu_open) # on affiche la simulation 
            self.ui.draw(self.screen, self.infos, self.vaccine_progression) # on affiche : textes, menus, icones
    
    
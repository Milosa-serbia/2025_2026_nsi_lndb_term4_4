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
        
        # Temps entre les updates des infos et de l'infection
        self.time_last_update = 0
        self.time_between_updates = 100 # ms
        
        # Premier pixel infecté au centre
        self.status_grid[self.height // 2, self.width // 2] = 1
        
        # Infos des états
        self.infos = {}
        for id in STATES.keys() :
            self.infos[id] = KinderState( \
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
        for id, state in self.infos.items() :
            state.alive_population = counts[id] * self.infos[id].population_per_px
            state.vegetable_production = (state.initial_vegetable_production / state.population) * state.alive_population
            state.food_ressources = state.food_ressources + state.vegetable_production - (state.alive_population * (1 + state.obesity_rate))
            for export_id, export_part in state.exportations.items() :
                state.food_ressources -= state.vegetable_production * export_part
                self.infos[export_id].food_ressources += state.vegetable_production * export_part
            
    
    
    def update_and_draw(self, events) :
        self.handle_input(events)
        if self.ui.menu_open :
            self.ui.handle_input(events)
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_update >= self.time_between_updates :
            self.time_last_update = current_time
            self.infection.update(self.status_grid, self.close_border_state, self.lockdowned_state)
            self.update_infos()
        self.infection.draw(self.screen, self.state_grid, self.status_grid, self.ui.menu_open)
        self.ui.draw(self.screen, self.infos)
    
    
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
        self.time_between_updates = 500 # ms
        
        # Premier pixel infecté aléatoire dans certains états
        start_states = [107, 108, 110, 113, 114, 115, 116, 119, 120, 121, 124, 125, 126]
        # on récupère tous les pixels qui appartiennent à ces états
        mask = np.isin(self.state_grid, start_states)
        ys, xs = np.where(mask)

        # on choisit un pixel au hasard parmi ces positions
        idx = np.random.randint(0, len(ys))
        y0, x0 = ys[idx], xs[idx]
        self.status_grid[y0, x0] = 1
        
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

        # pré-calcul des pixels de chaque état pour éviter np.argwhere à chaque update quand on doit appliquer la selection des morts de la famine (ENORMEEE GAIN DE PERF)
        self.state_pixels = {}
        for state_id in range(101, 147):  # IDs des vrais états
            coords = np.argwhere(self.state_grid == state_id)
            if coords.size == 0:
                ys = np.empty(0, dtype=int)
                xs = np.empty(0, dtype=int)
            else:
                ys = coords[:, 0]
                xs = coords[:, 1]
            self.state_pixels[state_id] = (ys, xs)


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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 :
                if self.ui.menu_open :
                    self.ui.menu_open = False
                if self.ui.menu2_open :
                    self.ui.menu2_open = False
                    
    
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

            if factor < 0:
                factor = 0  # sécurité au cas où

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
                # si l'id est 0 alors pas d'export défini
                if export_id == 0 or export_part <= 0 :
                    continue

                dest = self.infos[export_id]

                # quantité que l'état voudrait exporter pendant ce update
                wanted = state.initial_vegetable_production * export_part
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

        # ===== 4) Famine optimisée : tuer des pixels quand food_ressources == 0 =====
        for state_id, state in self.infos.items():
            # on ne traite que les vrais états
            if not (101 <= state_id <= 146):
                continue

            # si l'état a encore de la nourriture, rien ne se passe
            if state.food_ressources > 0:
                continue

            ys_all, xs_all = self.state_pixels.get(state_id, (None, None))
            if ys_all is None or ys_all.size == 0:
                continue

            # on regarde le statut de ces pixels dans status_grid
            status_sub = self.status_grid[ys_all, xs_all]

            # on ne tue que les pixels pas encore morts (status != 2)
            alive_mask = (status_sub != 2)
            if not np.any(alive_mask):
                continue

            ys_alive = ys_all[alive_mask]
            xs_alive = xs_all[alive_mask]

            # on tue jusqu'à 10 pixels
            n_to_kill = min(10, ys_alive.size)

            # choix aléatoire de n_to_kill indices parmi les pixels vivants
            idx = self.infection.rng.integers(
                0, ys_alive.size, size=n_to_kill, endpoint=False
            )

            self.status_grid[ys_alive[idx], xs_alive[idx]] = 2


    def end_game(self) :
            # On ferme les menus si ouverts
            self.ui.menu_open = False
            if hasattr(self.ui, "menu2_open") :
                self.ui.menu2_open = False

            # ==== CALCUL DES SCORES ====
            # population totale vivante (vrais états 101–146)
            alive_total = int(sum(
                st.alive_population
                for sid, st in self.infos.items()
                if 101 <= sid <= 146
            ))

            # population totale initiale
            total_initial = sum(
                STATES[id]['population']
                for id in STATES.keys()
                if 101 <= id <= 146
            )

            # score sur 100
            score = int(round((alive_total / total_initial) * 100))

            # ==== AFFICHAGE ====
            self.infection.draw(self.screen, self.state_grid, self.status_grid, False)

            # panneau centré
            w, h = self.screen.get_size()
            panel = pygame.Rect(w//2 - 350, h//2 - 150, 700, 300)

            pygame.draw.rect(self.screen, (0,0,0), panel.inflate(20,20), border_radius=15)
            pygame.draw.rect(self.screen, (240,240,240), panel, border_radius=15)

            # texte
            big_font = pygame.font.Font(None, 70)
            font = pygame.font.Font(None, 50)

            t1 = big_font.render("VACCIN TROUVÉ – FIN", True, (0,0,0))
            t2 = font.render(f"Population totale en vie : {alive_total}", True, (0,0,0))
            t3 = font.render(f"Score : {score} / 100", True, (0,0,0))

            self.screen.blit(t1, t1.get_rect(center=(panel.centerx, panel.top + 70)))
            self.screen.blit(t2, t2.get_rect(center=(panel.centerx, panel.top + 150)))
            self.screen.blit(t3, t3.get_rect(center=(panel.centerx, panel.top + 210)))
    
        


    def update_and_draw(self, events) :
        # ====================== JEU EN COURS ======================
        if self.vaccine_progression < 100 :
            prev_menu_open = self.ui.menu_open
            self.handle_input(events) # on gere les input hors menu
            if self.ui.menu_open and prev_menu_open :
                self.ui.handle_input(events) # on gere les input dans les menu
            current_time = pygame.time.get_ticks()
            if current_time - self.time_last_update >= self.time_between_updates : # on fait une update de l'infection et des etats a intervals de temps reguliers
                self.vaccine_progression += 0.115
                self.time_last_update = current_time
                self.infection.update(self.status_grid, self.close_border_state, self.lockdowned_state) # update de l'infection
                self.update_infos() # update des infos des etats
            self.infection.draw(self.screen, self.state_grid, self.status_grid, self.ui.menu_open) # on affiche la simulation 
            self.ui.draw(self.screen, self.infos, self.vaccine_progression) # on affiche : textes, menus, icones
            
        # ====================== FIN DE PARTIE ======================
        else :
            self.end_game()


    
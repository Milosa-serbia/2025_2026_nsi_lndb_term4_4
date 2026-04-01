import pygame
from brbr_infection import *
from brbr_ui import *

class Continent :
    def __init__(self, time_between_updates=500) :
        # Initialisation infos fenetre
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Status_grid : 0 = safe, 1 = infected, 2 = dead, 255 = border , 100 = sea, 101:146 = states
        self.status_grid = np.load('graphics/dessin.npy')
        self.state_grid = self.status_grid.copy()
        
        # progression du vaccin
        self.vaccine_progression = 0
        
        # Temps entre les updates des infos et de l'infection
        self.time_last_update = 0
        self.time_between_updates = time_between_updates
        
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

        # ===== 3) sécurité finale + mise à jour famine =====
        for state in self.infos.values() :
            if state.food_ressources < 0 :
                state.food_ressources = 0
            state.is_starving = (state.food_ressources == 0)

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
            alive_total = int(sum(
                st.alive_population
                for sid, st in self.infos.items()
                if 101 <= sid <= 146
            ))
            total_initial = sum(
                STATES[id]['population']
                for id in STATES.keys()
                if 101 <= id <= 146
            )
            dead_total = total_initial - alive_total
            score = int(round((alive_total / total_initial) * 100))

            # ==== AFFICHAGE ====
            self.infection.draw(self.screen, self.state_grid, self.status_grid, False)

            w, h = self.screen.get_size()

            # ---- Palette DA ----
            C_BG        = (12,  14,  20)
            C_PANEL     = (18,  22,  32)
            C_SURFACE   = (26,  32,  46)
            C_SURFACE2  = (32,  40,  58)
            C_BORDER    = (48,  60,  90)
            C_ACCENT    = (56, 189, 248)
            C_GREEN     = (99, 235, 167)
            C_DANGER    = (248,  82,  82)
            C_WARNING   = (251, 189,  35)
            C_TEXT      = (220, 228, 245)
            C_TEXT_DIM  = (100, 115, 150)

            # Couleur du score selon performance
            if score >= 75 :
                score_color = C_GREEN
                verdict     = "EXCELLENTE GESTION"
                verdict_col = C_GREEN
            elif score >= 50 :
                score_color = C_WARNING
                verdict     = "GESTION CORRECTE"
                verdict_col = C_WARNING
            elif score >= 25 :
                score_color = (255, 140, 50)
                verdict     = "GESTION INSUFFISANTE"
                verdict_col = (255, 140, 50)
            else :
                score_color = C_DANGER
                verdict     = "ÉCHEC CRITIQUE"
                verdict_col = C_DANGER

            # ---- Overlay sombre sur toute la carte ----
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((8, 10, 16, 200))
            self.screen.blit(overlay, (0, 0))

            # ---- Dimensions panneau principal ----
            PW, PH = 640, 420
            px = w // 2 - PW // 2
            py = h // 2 - PH // 2

            # Ombre portée
            shadow = pygame.Surface((PW + 40, PH + 40), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 120), shadow.get_rect(), border_radius=18)
            self.screen.blit(shadow, (px - 20 + 6, py - 20 + 8))

            # Fond du panneau
            panel_surf = pygame.Surface((PW, PH), pygame.SRCALPHA)
            pygame.draw.rect(panel_surf, (*C_PANEL, 252), panel_surf.get_rect(), border_radius=14)
            self.screen.blit(panel_surf, (px, py))

            # Bordure extérieure
            pygame.draw.rect(self.screen, C_BORDER, pygame.Rect(px, py, PW, PH), width=1, border_radius=14)

            # ---- En-tête ----
            header_h = 72
            header_surf = pygame.Surface((PW, header_h), pygame.SRCALPHA)
            pygame.draw.rect(header_surf, (*C_SURFACE2, 255), header_surf.get_rect(), border_radius=14)
            # masquer les coins inférieurs arrondis de l'en-tête
            pygame.draw.rect(header_surf, (*C_SURFACE2, 255), pygame.Rect(0, header_h - 14, PW, 14))
            self.screen.blit(header_surf, (px, py))

            # Barre accent verticale à gauche de l'en-tête
            pygame.draw.rect(self.screen, C_ACCENT, pygame.Rect(px, py, 4, header_h), border_radius=2)

            # Séparateur bas en-tête
            pygame.draw.line(self.screen, C_BORDER, (px, py + header_h), (px + PW, py + header_h), 1)

            # Petits points décoratifs en haut à droite
            for i in range(3) :
                dot_x = px + PW - 20 - i * 14
                pygame.draw.circle(self.screen, C_BORDER if i > 0 else C_ACCENT, (dot_x, py + header_h // 2), 4)

            font_title  = pygame.font.SysFont('consolas', 22, bold=True)
            font_sub    = pygame.font.SysFont('consolas', 14)
            font_label  = pygame.font.SysFont('consolas', 13)
            font_big    = pygame.font.SysFont('consolas', 52, bold=True)
            font_med    = pygame.font.SysFont('consolas', 20, bold=True)
            font_small  = pygame.font.SysFont('consolas', 15)

            t_title = font_title.render("RAPPORT DE FIN DE SIMULATION", True, C_TEXT)
            self.screen.blit(t_title, (px + 16, py + 14))
            t_sub = font_sub.render("BRBR Virus  ·  VACCIN DÉCOUVERT  ·  SIMULATION TERMINÉE", True, C_TEXT_DIM)
            self.screen.blit(t_sub, (px + 16, py + 44))

            # ---- Score central ----
            cy = py + header_h + 30
            score_str = f"{score:02d}"
            t_score = font_big.render(score_str, True, score_color)
            t_slash = font_big.render(" / 100", True, C_TEXT_DIM)
            total_w = t_score.get_width() + t_slash.get_width()
            self.screen.blit(t_score, (px + PW // 2 - total_w // 2, cy))
            self.screen.blit(t_slash, (px + PW // 2 - total_w // 2 + t_score.get_width(), cy))

            t_verdict = font_med.render(verdict, True, verdict_col)
            self.screen.blit(t_verdict, t_verdict.get_rect(centerx=px + PW // 2, top=cy + 68))

            # ---- Barre de score ----
            bar_y = cy + 110
            bar_x = px + 32
            bar_w = PW - 64
            bar_h = 10
            # fond barre
            pygame.draw.rect(self.screen, C_SURFACE2, pygame.Rect(bar_x, bar_y, bar_w, bar_h), border_radius=5)
            # remplissage
            fill_w = int(bar_w * score / 100)
            if fill_w > 0 :
                pygame.draw.rect(self.screen, score_color, pygame.Rect(bar_x, bar_y, fill_w, bar_h), border_radius=5)
            # marqueurs à 25, 50, 75
            for pct in [25, 50, 75] :
                mx = bar_x + int(bar_w * pct / 100)
                pygame.draw.line(self.screen, C_BORDER, (mx, bar_y - 3), (mx, bar_y + bar_h + 3), 1)

            # ---- Séparateur ----
            sep_y = bar_y + 30
            pygame.draw.line(self.screen, C_BORDER, (px + 24, sep_y), (px + PW - 24, sep_y), 1)

            # ---- Stats en 2 colonnes ----
            def draw_stat_block(label, value, val_color, col_x, row_y) :
                lbl = font_label.render(label, True, C_TEXT_DIM)
                val = font_small.render(value, True, val_color)
                self.screen.blit(lbl, (col_x, row_y))
                self.screen.blit(val, (col_x, row_y + 18))

            stats_y = sep_y + 16
            col1 = px + 40
            col2 = px + PW // 2 + 20

            draw_stat_block(
                "POPULATION EN VIE",
                f"{alive_total:,}".replace(",", " "),
                C_GREEN,
                col1, stats_y
            )
            draw_stat_block(
                "VICTIMES DE L'ÉPIDÉMIE",
                f"{dead_total:,}".replace(",", " "),
                C_DANGER,
                col2, stats_y
            )

            # Petit séparateur vertical entre les deux colonnes
            pygame.draw.line(
                self.screen, C_BORDER,
                (px + PW // 2, stats_y - 4),
                (px + PW // 2, stats_y + 46),
                1
            )

            # ---- Pied de panneau ----
            foot_y = py + PH - 44
            pygame.draw.line(self.screen, C_BORDER, (px + 24, foot_y), (px + PW - 24, foot_y), 1)
            pct_alive = alive_total / total_initial * 100
            t_foot = font_label.render(
                f"{pct_alive:.1f}% de la population initiale a survécu  ·  FERMER : ALT+F4",
                True, C_TEXT_DIM
            )
            self.screen.blit(t_foot, t_foot.get_rect(centerx=px + PW // 2, top=foot_y + 12))
    
        
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
            self.ui.draw(self.screen, self.infos, self.vaccine_progression, self.state_grid) # on affiche : textes, menus, icones
            
        # ====================== FIN DE PARTIE ======================
        else :
            self.end_game()
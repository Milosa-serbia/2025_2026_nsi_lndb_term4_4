import pygame
from brbr_data import *
import math


# ============================================================
#  PALETTE DE COULEURS GLOBALE
# ============================================================
C_BG          = (12,  14,  20)    # fond des panneaux
C_PANEL       = (18,  22,  32)    # panneau principal
C_SURFACE     = (26,  32,  46)    # surfaces internes
C_SURFACE2    = (32,  40,  58)    # surfaces légèrement plus claires
C_BORDER      = (48,  60,  90)    # bordures subtiles
C_ACCENT      = (56, 189, 248)    # bleu cyan vif (accent principal)
C_ACCENT2     = (99, 235, 167)    # vert mint (succès / vivant)
C_DANGER      = (248,  82,  82)   # rouge danger
C_WARNING     = (251, 189,  35)   # orange/jaune avertissement
C_TEXT        = (220, 228, 245)   # texte principal
C_TEXT_DIM    = (100, 115, 150)   # texte secondaire
C_WHITE       = (255, 255, 255)


def draw_rounded_rect(surface, color, rect, radius=8, alpha=255):
    """Dessine un rectangle arrondi avec transparence optionnelle."""
    if alpha < 255:
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(tmp, (*color, alpha), tmp.get_rect(), border_radius=radius)
        surface.blit(tmp, rect.topleft)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_border_rect(surface, color, rect, width=1, radius=8):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)


def lerp_color(color_a, color_b, t):
    """Interpole linéairement entre deux couleurs selon t (entre 0 et 1)."""
    r = int(color_a[0] + (color_b[0] - color_a[0]) * t)
    g = int(color_a[1] + (color_b[1] - color_a[1]) * t)
    b = int(color_a[2] + (color_b[2] - color_a[2]) * t)
    return (r, g, b)


# ============================================================
#  BOUTON PRINCIPAL (menu 1)
# ============================================================
class Button:
    def __init__(self, x, y, width, height, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click
        self.hover_animation = 0.0  # valeur entre 0 et 1 pour l'animation de survol

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, text, active=False):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # animation douce vers 1.0 si survolé, vers 0.0 sinon
        hover_target = 1.0 if is_hovered else 0.0
        self.hover_animation += (hover_target - self.hover_animation) * 0.25

        # couleurs selon l'état actif ou non
        if active:
            bg_color = lerp_color(C_ACCENT, (80, 210, 255), self.hover_animation)
            border_color = C_ACCENT
            text_color = C_BG
        else:
            bg_color = lerp_color(C_SURFACE2, C_SURFACE, self.hover_animation)
            border_color = lerp_color(C_BORDER, C_ACCENT, self.hover_animation)
            text_color = lerp_color(C_TEXT_DIM, C_TEXT, self.hover_animation)

        draw_rounded_rect(screen, bg_color, self.rect, radius=6)
        draw_border_rect(screen, border_color, self.rect, width=1, radius=6)

        # texte du bouton, aligné à gauche
        label_x = self.rect.x + 12
        label_surf = self.font.render(text if text else '—', True, text_color)
        screen.blit(label_surf, label_surf.get_rect(midleft=(label_x, self.rect.centery)))

        # petite flèche à droite
        arrow_color = lerp_color(C_TEXT_DIM, C_ACCENT, self.hover_animation)
        arrow_surf = self.font.render('›', True, arrow_color)
        screen.blit(arrow_surf, arrow_surf.get_rect(midright=(self.rect.right - 10, self.rect.centery)))


# ============================================================
#  BOUTON DU MENU 2 (liste déroulante)
# ============================================================
class Menu2Button:
    def __init__(self, x, y, width, height, font, text, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.on_click = on_click
        self.hover_animation = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, selected=False):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        hover_target = 1.0 if (is_hovered or selected) else 0.0
        self.hover_animation += (hover_target - self.hover_animation) * 0.25

        if selected:
            bg_color = lerp_color(C_SURFACE2, C_ACCENT, 0.25)
            text_color = C_ACCENT
        else:
            bg_color = lerp_color(C_SURFACE, C_SURFACE2, self.hover_animation)
            text_color = lerp_color(C_TEXT_DIM, C_TEXT, self.hover_animation)

        draw_rounded_rect(screen, bg_color, self.rect, radius=4)
        if is_hovered or selected:
            pygame.draw.line(screen, C_ACCENT, self.rect.topleft, self.rect.bottomleft, 2)

        label_surf = self.font.render(self.text, True, text_color)
        screen.blit(label_surf, label_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery)))


# ============================================================
#  BOUTON TOGGLE (frontières / confinement)
# ============================================================
class ToggleButton:
    def __init__(self, x, y, width, height, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click
        self.hover_animation = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, active):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        hover_target = 1.0 if is_hovered else 0.0
        self.hover_animation += (hover_target - self.hover_animation) * 0.25

        if active:
            bg_color = lerp_color((30, 60, 40), (40, 90, 55), self.hover_animation)
            border_color = C_ACCENT2
            dot_color = C_ACCENT2
            label_text = 'ACTIF'
            text_color = C_ACCENT2
        else:
            bg_color = lerp_color(C_SURFACE, C_SURFACE2, self.hover_animation)
            border_color = lerp_color(C_BORDER, C_TEXT_DIM, self.hover_animation)
            dot_color = C_TEXT_DIM
            label_text = 'INACTIF'
            text_color = C_TEXT_DIM

        draw_rounded_rect(screen, bg_color, self.rect, radius=6)
        draw_border_rect(screen, border_color, self.rect, width=1, radius=6)

        # dessin du toggle (pilule + point)
        pill_width = 36
        pill_height = 18
        pill_x = self.rect.x + 10
        pill_y = self.rect.centery - pill_height // 2
        pill_rect = pygame.Rect(pill_x, pill_y, pill_width, pill_height)
        draw_rounded_rect(screen, bg_color, pill_rect, radius=9)
        draw_border_rect(screen, border_color, pill_rect, width=1, radius=9)

        # position du point : à droite si actif, à gauche sinon
        if active:
            dot_center_x = pill_x + (pill_width - 10)
        else:
            dot_center_x = pill_x + 10
        dot_center_y = pill_y + pill_height // 2
        pygame.draw.circle(screen, dot_color, (dot_center_x, dot_center_y), 7)

        label_surf = self.font.render(label_text, True, text_color)
        screen.blit(label_surf, label_surf.get_rect(midleft=(pill_x + pill_width + 8, self.rect.centery)))


# ============================================================
#  PANNEAU SCROLLABLE (menu 2 — liste des états destinataires)
# ============================================================
class ScrollablePanel:
    """Panneau avec liste scrollable pour choisir un état destinataire."""
    PADDING_TOP = 5  # espace au-dessus du premier item

    def __init__(self, x, y, width, height, font, items, on_select):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.items = items      # liste de tuples (id, nom)
        self.on_select = on_select
        self.scroll_y = 0
        self.item_height = 30

        # hauteur totale du contenu (items + padding haut et bas)
        total_content_height = len(items) * self.item_height + self.PADDING_TOP * 2
        # scroll max = ce qui dépasse la zone visible
        self.max_scroll = max(0, total_content_height - height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - event.y * 20))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self.rect.collidepoint(mouse_x, mouse_y):
                # position relative dans le contenu scrollé
                relative_y = mouse_y - self.rect.y + self.scroll_y - self.PADDING_TOP
                clicked_index = relative_y // self.item_height
                if 0 <= clicked_index < len(self.items):
                    self.on_select(self.items[clicked_index][0])

    def draw(self, screen, selected_id=None):
        draw_rounded_rect(screen, C_PANEL, self.rect, radius=8)
        draw_border_rect(screen, C_BORDER, self.rect, width=1, radius=8)

        # on restreint le dessin à la zone du panneau (clipping)
        old_clip = screen.get_clip()
        screen.set_clip(self.rect.inflate(-2, -2))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for index, (state_id, state_name) in enumerate(self.items):
            # position verticale de l'item dans le panneau
            item_y = self.rect.y + self.PADDING_TOP + index * self.item_height - self.scroll_y

            # on saute les items hors de la zone visible
            if item_y + self.item_height < self.rect.y:
                continue
            if item_y > self.rect.bottom:
                continue

            item_rect = pygame.Rect(self.rect.x + 4, item_y, self.rect.width - 8, self.item_height - 2)
            is_hovered = item_rect.collidepoint(mouse_x, mouse_y)
            is_selected = (state_id == selected_id)

            if is_selected:
                draw_rounded_rect(screen, lerp_color(C_SURFACE2, C_ACCENT, 0.2), item_rect, radius=4)
                pygame.draw.line(screen, C_ACCENT, item_rect.topleft, item_rect.bottomleft, 2)
                text_color = C_ACCENT
            elif is_hovered:
                draw_rounded_rect(screen, C_SURFACE2, item_rect, radius=4)
                text_color = C_TEXT
            else:
                text_color = C_TEXT_DIM

            label_surf = self.font.render(state_name, True, text_color)
            screen.blit(label_surf, label_surf.get_rect(midleft=(item_rect.x + 10, item_rect.centery)))

        screen.set_clip(old_clip)

        # scrollbar verticale si le contenu dépasse
        total_content_height = len(self.items) * self.item_height
        if total_content_height > self.rect.height:
            scrollbar_height = max(30, int(self.rect.height * self.rect.height / total_content_height))
            if self.max_scroll > 0:
                scrollbar_y = self.rect.y + int(self.scroll_y * (self.rect.height - scrollbar_height) / self.max_scroll)
            else:
                scrollbar_y = self.rect.y
            scrollbar_rect = pygame.Rect(self.rect.right - 6, scrollbar_y, 4, scrollbar_height)
            draw_rounded_rect(screen, C_BORDER, scrollbar_rect, radius=2)


# ============================================================
#  SÉLECTEUR DE POURCENTAGE (rangée de boutons %)
# ============================================================
class PercentSelector:
    def __init__(self, x, y, width, font, on_select):
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.on_select = on_select
        self.percent_values = list(range(0, 110, 10))
        self.btn_w = (width - (len(self.percent_values) - 1) * 4) // len(self.percent_values)
        self.hover_animations = [0.0] * len(self.percent_values)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, percent in enumerate(self.percent_values):
                btn_rect = pygame.Rect(self.x + index * (self.btn_w + 4), self.y, self.btn_w, 30)
                if btn_rect.collidepoint(event.pos):
                    self.on_select(percent)

    def draw(self, screen, current_value):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for index, percent in enumerate(self.percent_values):
            btn_rect = pygame.Rect(self.x + index * (self.btn_w + 4), self.y, self.btn_w, 30)
            is_selected = (current_value is not None and int(current_value * 100) == percent)
            is_hovered = btn_rect.collidepoint(mouse_x, mouse_y)

            hover_target = 1.0 if (is_hovered or is_selected) else 0.0
            self.hover_animations[index] += (hover_target - self.hover_animations[index]) * 0.25

            if is_selected:
                bg_color = C_ACCENT
                text_color = C_BG
            else:
                bg_color = lerp_color(C_SURFACE, C_SURFACE2, self.hover_animations[index])
                text_color = lerp_color(C_TEXT_DIM, C_TEXT, self.hover_animations[index])

            draw_rounded_rect(screen, bg_color, btn_rect, radius=4)
            border_color = lerp_color(C_BORDER, C_ACCENT, self.hover_animations[index])
            draw_border_rect(screen, border_color, btn_rect, width=1, radius=4)

            label_surf = self.font.render(f'{percent}', True, text_color)
            screen.blit(label_surf, label_surf.get_rect(center=btn_rect.center))


# ============================================================
#  FONCTIONS UTILITAIRES DE DESSIN
# ============================================================
def draw_label(screen, font, text, x, y, color=C_TEXT_DIM):
    label_surf = font.render(text, True, color)
    screen.blit(label_surf, (x, y))
    return label_surf.get_height()


def draw_stat_row(screen, font, label_text, value_text, x, y, value_color=C_TEXT):
    label_surf = font.render(label_text, True, C_TEXT_DIM)
    value_surf = font.render(str(value_text), True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x + label_surf.get_width() + 6, y))


def draw_section_header(screen, font, text, x, y, width):
    header_surf = font.render(text.upper(), True, C_ACCENT)
    screen.blit(header_surf, (x, y))
    line_y = y + header_surf.get_height() + 3
    pygame.draw.line(screen, C_BORDER, (x, line_y), (x + width, line_y), 1)
    return header_surf.get_height() + 8


def draw_progress_bar(screen, x, y, width, height, value, max_value, fill_color, bg_color=C_SURFACE):
    bar_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(screen, bg_color, bar_rect, radius=height // 2)
    fill_width = max(0, min(width, int(width * value / max_value)))
    if fill_width > 0:
        fill_rect = pygame.Rect(x, y, fill_width, height)
        draw_rounded_rect(screen, fill_color, fill_rect, radius=height // 2)
    draw_border_rect(screen, C_BORDER, bar_rect, width=1, radius=height // 2)


# ============================================================
#  CLASSE UI PRINCIPALE
# ============================================================
class UI:
    def __init__(self, infos, closed_border_states, lockdowned_states):
        self.px_id = None
        self.closed_border_states = closed_border_states
        self.lockdowned_states = lockdowned_states

        # Polices
        self.font_sm   = pygame.font.Font(None, 22)
        self.font      = pygame.font.Font(None, 26)
        self.font_md   = pygame.font.Font(None, 30)
        self.font_lg   = pygame.font.Font(None, 42)
        self.font_xl   = pygame.font.Font(None, 52)

        # Menu principal (panneau gauche)
        self.menu_open = False
        self.PANEL_W   = 360
        self.PANEL_H   = 820
        self.menu_rect = pygame.Rect(10, 15, self.PANEL_W, self.PANEL_H)

        # Menu 2 (panneau droit — choix d'exportation)
        self.menu2_open = False
        self.PANEL2_W   = 380
        self.menu2_rect = pygame.Rect(380, 15, self.PANEL2_W, self.PANEL_H)
        self.exportation_index = None

        # Liste des états pour le menu 2 (id=0 pour "aucun"), triée alphabétiquement
        sorted_states = sorted(
            [(state_id, infos[state_id].name) for state_id in range(101, 147)],
            key=lambda item: item[1]
        )
        self.state_list = [(0, '— Aucun —')] + sorted_states

        # Panneau scrollable dans le menu 2
        self.state_scroll = ScrollablePanel(
            self.menu2_rect.x + 10,
            self.menu2_rect.y + 90,
            self.PANEL2_W - 20,
            500,
            self.font,
            self.state_list,
            on_select=lambda selected_id: self.change_exportation_id(infos, selected_id)
        )

        # Sélecteur de pourcentage dans le menu 2
        self.percent_sel = PercentSelector(
            self.menu2_rect.x + 10,
            self.menu2_rect.y + 620,
            self.PANEL2_W - 20,
            self.font_sm,
            on_select=lambda percent: self.change_exportations_percent(infos, percent)
        )

        # Boutons d'export (4 slots) dans le menu principal
        slot_x = self.menu_rect.x + 14
        self.exportation_buttons = [
            Button(slot_x,       self.menu_rect.y + 355, 155, 32, self.font, lambda i=0: self.open_menu2(i)),
            Button(slot_x + 163, self.menu_rect.y + 355, 155, 32, self.font, lambda i=1: self.open_menu2(i)),
            Button(slot_x,       self.menu_rect.y + 395, 155, 32, self.font, lambda i=2: self.open_menu2(i)),
            Button(slot_x + 163, self.menu_rect.y + 395, 155, 32, self.font, lambda i=3: self.open_menu2(i)),
        ]

        # Boutons toggle (frontières / confinement)
        self.border_button = ToggleButton(
            self.menu_rect.x + 14, self.menu_rect.y + 460, 300, 34, self.font,
            lambda: self.change_border_statue(infos, self.closed_border_states)
        )
        self.lockdown_button = ToggleButton(
            self.menu_rect.x + 14, self.menu_rect.y + 504, 300, 34, self.font,
            lambda: self.change_lockdown_statue(infos, self.lockdowned_states)
        )

        # Chargement des icônes
        self.lockdown_image = pygame.image.load("Enter.png").convert_alpha()
        self.lockdown_image = pygame.transform.scale(self.lockdown_image, (22, 22))
        self.closed_border_image = pygame.image.load("Locked.png").convert_alpha()
        self.closed_border_image = pygame.transform.scale(self.closed_border_image, (22, 22))
        self.closed_border_and_lockdown_image = pygame.image.load("Power.png").convert_alpha()
        self.closed_border_and_lockdown_image = pygame.transform.scale(self.closed_border_and_lockdown_image, (22, 22))
        self.scientist_image = pygame.image.load("Scientist.png").convert_alpha()
        self.scientist_image = pygame.transform.scale(self.scientist_image, (48, 48))

        # Surface de vignette (assombrissement des bords de l'écran)
        screen = pygame.display.get_surface()
        self.vignette_surface = self._make_vignette(screen.get_width(), screen.get_height())

    # ------------------------------------------------------------------
    def _make_vignette(self, screen_width, screen_height):
        """Crée une surface noire transparente plus opaque sur les bords."""
        surf = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        for i in range(60):
            alpha = int(120 * (1 - i / 60) ** 2)
            pygame.draw.rect(surf, (0, 0, 0, alpha), (i, i, screen_width - 2*i, screen_height - 2*i), 1)
        return surf

    # ------------------------------------------------------------------
    #  ACTIONS
    # ------------------------------------------------------------------
    def change_border_statue(self, infos, closed_border_states):
        if self.px_id in closed_border_states:
            closed_border_states.remove(self.px_id)
            infos[self.px_id].closed_border = False
        else:
            if len(closed_border_states) < 4:
                closed_border_states.append(self.px_id)
                infos[self.px_id].closed_border = True

    def change_lockdown_statue(self, infos, lockdowned_states):
        if self.px_id in lockdowned_states:
            lockdowned_states.remove(self.px_id)
            infos[self.px_id].lockdown = False
        else:
            if len(lockdowned_states) < 4:
                lockdowned_states.append(self.px_id)
                infos[self.px_id].lockdown = True

    def change_exportation_id(self, infos, new_export_id):
        if self.px_id is None or self.exportation_index is None:
            return
        current_state = infos[self.px_id]
        old_export_id = current_state.exportations[self.exportation_index][0]

        # on retire l'ancienne importation chez l'ancien destinataire
        if old_export_id != 0:
            try:
                infos[old_export_id].importations.remove(current_state.name)
            except ValueError:
                pass

        # on met à jour l'exportation (destination + reset du pourcentage)
        current_state.exportations[self.exportation_index][0] = new_export_id
        current_state.exportations[self.exportation_index][1] = 0

        # on enregistre la nouvelle importation chez le nouveau destinataire
        if new_export_id != 0:
            infos[new_export_id].importations.append(current_state.name)

    def change_exportations_percent(self, infos, percent):
        if self.px_id is None or self.exportation_index is None:
            return
        infos[self.px_id].exportations[self.exportation_index][1] = percent / 100

    def open_menu2(self, exportation_index):
        if not self.menu2_open:
            self.exportation_index = exportation_index
            self.menu2_open = True
        elif self.exportation_index == exportation_index:
            self.menu2_open = False
        else:
            self.exportation_index = exportation_index

    # ------------------------------------------------------------------
    #  GESTION DES INPUTS
    # ------------------------------------------------------------------
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.exportation_buttons:
                    btn.handle_event(event)
                self.border_button.handle_event(event)
                self.lockdown_button.handle_event(event)
                if self.menu2_open:
                    self.state_scroll.handle_event(event)
                    self.percent_sel.handle_event(event)
            if event.type == pygame.MOUSEWHEEL:
                if self.menu2_open:
                    self.state_scroll.handle_event(event)

    # ------------------------------------------------------------------
    #  DESSIN PRINCIPAL
    # ------------------------------------------------------------------
    def draw(self, screen, infos, vaccine_progression, state_grid=None):
        screen.blit(self.vignette_surface, (0, 0))
        self._draw_vaccine_bar(screen, vaccine_progression)
        self._draw_state_icons(screen, infos)

        if state_grid is not None and not self.menu_open:
            self._draw_hover_tooltip(screen, infos, state_grid)

        if self.menu_open and self.px_id is not None:
            self._draw_main_panel(screen, infos)

        if self.menu2_open and self.menu_open:
            self._draw_menu2(screen, infos)

    # ------------------------------------------------------------------
    def _draw_hover_tooltip(self, screen, infos, state_grid):
        """Affiche un tooltip en bas de l'écran quand on survole un état."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_width, screen_height = screen.get_size()

        if not (0 <= mouse_y < state_grid.shape[0] and 0 <= mouse_x < state_grid.shape[1]):
            return

        state_id = state_grid[mouse_y, mouse_x]
        if not (101 <= state_id <= 146) or state_id not in infos:
            return

        hovered_state = infos[state_id]

        name_text = hovered_state.name
        if hovered_state.is_starving:
            status_text = 'FAMINE — les habitants meurent de faim'
            status_color = C_DANGER
        else:
            status_text = None

        # calcul des dimensions du tooltip
        name_surf = self.font_md.render(name_text, True, C_WHITE)
        padding_x = 24
        padding_y = 10
        tooltip_width = name_surf.get_width() + padding_x * 2
        tooltip_height = name_surf.get_height() + padding_y * 2

        status_surf = None
        if status_text:
            status_surf = self.font_sm.render(status_text, True, status_color)
            tooltip_width = max(tooltip_width, status_surf.get_width() + padding_x * 2)
            tooltip_height += status_surf.get_height() + 6

        # position centrée en bas de l'écran
        margin_bottom = 14
        tooltip_x = screen_width // 2 - tooltip_width // 2
        tooltip_y = screen_height - tooltip_height - margin_bottom
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)

        draw_rounded_rect(screen, C_PANEL, tooltip_rect, radius=10, alpha=220)
        draw_border_rect(screen, C_BORDER, tooltip_rect, width=1, radius=10)

        # barre colorée en haut du tooltip
        accent_bar = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, 3)
        if status_surf:
            draw_rounded_rect(screen, C_DANGER, accent_bar, radius=2)
        else:
            draw_rounded_rect(screen, C_ACCENT, accent_bar, radius=2)

        # texte
        current_y = tooltip_y + padding_y
        screen.blit(name_surf, name_surf.get_rect(centerx=tooltip_x + tooltip_width // 2, y=current_y))
        current_y += name_surf.get_height() + 6
        if status_surf:
            screen.blit(status_surf, status_surf.get_rect(centerx=tooltip_x + tooltip_width // 2, y=current_y))

    # ------------------------------------------------------------------
    def _draw_vaccine_bar(self, screen, vaccine_progression):
        """Affiche la barre de progression du vaccin en haut à droite."""
        bar_x = 1050
        bar_y = 14
        bar_width = 380
        bar_height = 46

        # fond du panneau
        panel_rect = pygame.Rect(bar_x - 10, bar_y - 4, bar_width + 20, bar_height + 8)
        draw_rounded_rect(screen, C_PANEL, panel_rect, radius=10, alpha=210)
        draw_border_rect(screen, C_BORDER, panel_rect, width=1, radius=10)

        # icône du scientifique
        screen.blit(self.scientist_image, (bar_x - 8, bar_y - 2))

        # label
        label_surf = self.font_sm.render('VACCIN EN COURS :', True, C_TEXT_DIM)
        screen.blit(label_surf, (bar_x + 46, bar_y + 2))

        # barre de progression
        progress_rect = pygame.Rect(bar_x + 46, bar_y + 20, bar_width - 56, 14)
        draw_rounded_rect(screen, C_SURFACE, progress_rect, radius=7)
        fill_width = int((bar_width - 56) * vaccine_progression / 100)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x + 46, bar_y + 20, fill_width, 14)
            draw_rounded_rect(screen, C_ACCENT, fill_rect, radius=7)
        draw_border_rect(screen, C_BORDER, progress_rect, width=1, radius=7)

        # pourcentage affiché dans la barre
        pct_surf = self.font_sm.render(f'{int(vaccine_progression)}%', True, C_WHITE)
        screen.blit(pct_surf, pct_surf.get_rect(midright=(progress_rect.right - 140, bar_y + 10)))

    # ------------------------------------------------------------------
    def _draw_state_icons(self, screen, infos):
        """Affiche les icônes de confinement / frontières fermées sur la carte."""
        # on travaille sur une copie pour ne pas modifier la liste originale
        remaining_closed_borders = self.closed_border_states.copy()

        for state_id in self.lockdowned_states:
            icon_pos = infos[state_id].ui_pos
            if not icon_pos:
                continue
            if state_id not in remaining_closed_borders:
                # seulement en confinement
                screen.blit(self.lockdown_image, (icon_pos[0] - 4, icon_pos[1] - 4))
            else:
                # confinement ET frontières fermées
                remaining_closed_borders.remove(state_id)
                screen.blit(self.closed_border_and_lockdown_image, (icon_pos[0] - 4, icon_pos[1] - 4))

        for state_id in remaining_closed_borders:
            icon_pos = infos[state_id].ui_pos
            if icon_pos:
                screen.blit(self.closed_border_image, (icon_pos[0] - 4, icon_pos[1] - 4))

    # ------------------------------------------------------------------
    def _draw_main_panel(self, screen, infos):
        """Dessine le panneau principal (menu 1) avec les infos de l'état sélectionné."""
        state_infos = infos[self.px_id]
        panel = self.menu_rect

        # ombre et fond
        shadow_rect = panel.inflate(8, 8).move(4, 4)
        draw_rounded_rect(screen, (0, 0, 0), shadow_rect, radius=14, alpha=120)
        draw_rounded_rect(screen, C_PANEL, panel, radius=12, alpha=245)
        draw_border_rect(screen, C_BORDER, panel, width=1, radius=12)

        # en-tête coloré
        header_rect = pygame.Rect(panel.x, panel.y, panel.width, 68)
        draw_rounded_rect(screen, C_SURFACE2, header_rect, radius=12)
        pygame.draw.rect(screen, C_SURFACE2, pygame.Rect(panel.x, panel.y + 40, panel.width, 28))
        accent_bar = pygame.Rect(panel.x, panel.y, 4, 68)
        draw_rounded_rect(screen, C_ACCENT, accent_bar, radius=2)

        title_surf = self.font_lg.render(state_infos.name, True, C_WHITE)
        screen.blit(title_surf, (panel.x + 18, panel.y + 12))
        state_id_surf = self.font_sm.render(f'ID ÉTAT  ·  #{self.px_id}', True, C_TEXT_DIM)
        screen.blit(state_id_surf, (panel.x + 18, panel.y + 48))

        # constantes de mise en page
        MARGIN_H   = 18   # marge horizontale
        SEC_BEFORE = 14   # espace avant un titre de section
        SEC_AFTER  = 10   # espace après un titre de section
        ROW_HEIGHT = 24   # hauteur d'une ligne de stat
        BTN_HEIGHT = 36   # hauteur des boutons

        current_y = panel.y + 78

        # ---- Section Population ----
        current_y += SEC_BEFORE
        current_y += draw_section_header(screen, self.font_sm, '  Population', panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2)
        current_y += SEC_AFTER

        total_population = state_infos.population
        alive_population = int(state_infos.alive_population)
        dead_population = total_population - alive_population
        pct_alive = alive_population / total_population if total_population else 0

        draw_progress_bar(screen, panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2, 12, alive_population, total_population, C_ACCENT2)
        current_y += 20

        draw_stat_row(screen, self.font_sm, 'Vivants :', f'{alive_population:,}', panel.x + MARGIN_H, current_y, C_ACCENT2)
        draw_stat_row(screen, self.font_sm, 'Morts / inf. :', f'{dead_population:,}', panel.x + MARGIN_H + 170, current_y, C_DANGER)
        current_y += ROW_HEIGHT

        pct_surf = self.font_sm.render(f'{pct_alive*100:.1f}% de la population initiale survit', True, C_TEXT_DIM)
        screen.blit(pct_surf, (panel.x + MARGIN_H, current_y))
        current_y += ROW_HEIGHT + 4

        # ---- Section Santé & Ressources ----
        current_y += SEC_BEFORE
        current_y += draw_section_header(screen, self.font_sm, '  Santé & Ressources', panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2)
        current_y += SEC_AFTER

        draw_stat_row(screen, self.font_sm, "Obésité :", f"{state_infos.obesity_rate*100:.1f}%", panel.x + MARGIN_H, current_y)
        draw_stat_row(screen, self.font_sm, 'Prod. végétale :', f'{int(state_infos.vegetable_production):,}', panel.x + MARGIN_H + 130, current_y)
        current_y += ROW_HEIGHT + 4

        # barre réserves alimentaires
        food_max = max(state_infos.population * 100, state_infos.food_ressources + 1)
        if state_infos.food_ressources > state_infos.population * 20:
            food_bar_color = C_ACCENT2
        elif state_infos.food_ressources > 0:
            food_bar_color = C_WARNING
        else:
            food_bar_color = C_DANGER
        draw_progress_bar(screen, panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2, 12, state_infos.food_ressources, food_max, food_bar_color)
        current_y += 20

        draw_stat_row(screen, self.font_sm, 'Réserves alim. :', f'{int(state_infos.food_ressources):,}', panel.x + MARGIN_H, current_y, food_bar_color)
        current_y += ROW_HEIGHT + 4

        # ---- Section Exportations ----
        current_y += SEC_BEFORE
        current_y += draw_section_header(screen, self.font_sm, '  Exportations (4 slots)', panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2)
        current_y += SEC_AFTER

        slot_labels = ['Slot A', 'Slot B', 'Slot C', 'Slot D']
        slot_width = (panel.width - MARGIN_H*2 - 10) // 2
        slot_positions_x = [panel.x + MARGIN_H, panel.x + MARGIN_H + slot_width + 10]

        for slot_index, export_btn in enumerate(self.exportation_buttons):
            # 2 colonnes, 2 lignes → ligne = slot_index // 2, colonne = slot_index % 2
            row_y = current_y + (slot_index // 2) * (14 + BTN_HEIGHT + 8)
            col_x = slot_positions_x[slot_index % 2]

            export_destination_id = state_infos.exportations[slot_index][0]
            export_destination_name = infos[export_destination_id].name if export_destination_id != 0 else ''
            export_percent = int(state_infos.exportations[slot_index][1] * 100)

            # label du slot au-dessus du bouton
            if export_destination_id != 0:
                slot_label_text = f'{slot_labels[slot_index]}  —  {export_percent}%'
            else:
                slot_label_text = slot_labels[slot_index]
            slot_label_surf = self.font_sm.render(slot_label_text, True, C_TEXT_DIM)
            screen.blit(slot_label_surf, (col_x, row_y))

            # bouton sous le label
            export_btn.rect.x = col_x
            export_btn.rect.y = row_y + 16
            export_btn.rect.width = slot_width
            export_btn.rect.height = BTN_HEIGHT
            is_this_slot_open = self.menu2_open and self.exportation_index == slot_index
            export_btn.draw(screen, export_destination_name, active=is_this_slot_open)

        current_y += 2 * (14 + BTN_HEIGHT + 8) + 4

        # ---- Section Mesures sanitaires ----
        current_y += SEC_BEFORE
        current_y += draw_section_header(screen, self.font_sm, '  Mesures sanitaires', panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2)
        current_y += SEC_AFTER

        # Bouton frontières
        border_label_surf = self.font_sm.render('Fermer les frontières', True, C_TEXT_DIM)
        screen.blit(border_label_surf, (panel.x + MARGIN_H, current_y))
        current_y += 16
        self.border_button.rect.x = panel.x + MARGIN_H
        self.border_button.rect.y = current_y
        self.border_button.rect.width = panel.width - MARGIN_H*2
        self.border_button.rect.height = BTN_HEIGHT
        self.border_button.draw(screen, state_infos.closed_border)
        current_y += BTN_HEIGHT + 12

        # Bouton confinement
        lockdown_label_surf = self.font_sm.render('Confinement', True, C_TEXT_DIM)
        screen.blit(lockdown_label_surf, (panel.x + MARGIN_H, current_y))
        current_y += 16
        self.lockdown_button.rect.x = panel.x + MARGIN_H
        self.lockdown_button.rect.y = current_y
        self.lockdown_button.rect.width = panel.width - MARGIN_H*2
        self.lockdown_button.rect.height = BTN_HEIGHT
        self.lockdown_button.draw(screen, state_infos.lockdown)
        current_y += BTN_HEIGHT + 8

        # ---- Section Importations ----
        current_y += SEC_BEFORE
        current_y += draw_section_header(screen, self.font_sm, '  Importations reçues', panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2)
        current_y += SEC_AFTER - 5

        if state_infos.importations:
            for import_name in state_infos.importations:
                chip_rect = pygame.Rect(panel.x + MARGIN_H, current_y, panel.width - MARGIN_H*2, ROW_HEIGHT - 2)
                draw_rounded_rect(screen, C_SURFACE2, chip_rect, radius=4)
                pygame.draw.line(screen, C_ACCENT2, chip_rect.topleft, chip_rect.bottomleft, 2)
                chip_surf = self.font_sm.render(f'- {import_name}', True, C_ACCENT2)
                screen.blit(chip_surf, chip_surf.get_rect(midleft=(chip_rect.x + 10, chip_rect.centery)))
                current_y += ROW_HEIGHT + 4
        else:
            no_import_surf = self.font_sm.render('Aucune importation active', True, C_TEXT_DIM)
            screen.blit(no_import_surf, (panel.x + MARGIN_H, current_y))

    # ------------------------------------------------------------------
    def _draw_menu2(self, screen, infos):
        """Dessine le menu 2 : choix de l'état destinataire d'une exportation."""
        if self.px_id is None or self.exportation_index is None:
            return

        panel = self.menu2_rect
        state_infos = infos[self.px_id]
        slot_labels = ['Slot A', 'Slot B', 'Slot C', 'Slot D']

        # ombre et fond
        shadow_rect = panel.inflate(8, 8).move(4, 4)
        draw_rounded_rect(screen, (0, 0, 0), shadow_rect, radius=14, alpha=100)
        draw_rounded_rect(screen, C_PANEL, panel, radius=12, alpha=245)
        draw_border_rect(screen, C_BORDER, panel, width=1, radius=12)

        # en-tête
        header_rect = pygame.Rect(panel.x, panel.y, panel.width, 68)
        draw_rounded_rect(screen, C_SURFACE2, header_rect, radius=12)
        pygame.draw.rect(screen, C_SURFACE2, pygame.Rect(panel.x, panel.y + 40, panel.width, 28))
        accent_bar = pygame.Rect(panel.x, panel.y, 4, 68)
        draw_rounded_rect(screen, (99, 235, 167), accent_bar, radius=2)

        title_surf = self.font_lg.render(f'Exportation · {slot_labels[self.exportation_index]}', True, C_WHITE)
        screen.blit(title_surf, (panel.x + 16, panel.y + 12))
        subtitle_surf = self.font_sm.render(f'Destination depuis {state_infos.name}', True, C_TEXT_DIM)
        screen.blit(subtitle_surf, (panel.x + 16, panel.y + 48))

        # liste des états
        current_y = panel.y + 78
        list_label_surf = self.font_sm.render('ÉTAT DESTINATAIRE', True, C_TEXT_DIM)
        screen.blit(list_label_surf, (panel.x + 14, current_y))
        current_y += 20

        self.state_scroll.rect.y = current_y
        self.state_scroll.rect.x = panel.x + 10
        self.state_scroll.rect.width = panel.width - 20
        self.state_scroll.rect.height = 480

        current_selection_id = state_infos.exportations[self.exportation_index][0]
        self.state_scroll.draw(screen, selected_id=current_selection_id)

        current_y = self.state_scroll.rect.bottom + 16

        # sélecteur de pourcentage
        pct_label_surf = self.font_sm.render('POURCENTAGE DE PRODUCTION EXPORTÉ (%)', True, C_TEXT_DIM)
        screen.blit(pct_label_surf, (panel.x + 14, current_y))
        current_y += 20

        self.percent_sel.x = panel.x + 10
        self.percent_sel.y = current_y
        self.percent_sel.btn_w = (panel.width - 20 - (len(self.percent_sel.percent_values) - 1) * 4) // len(self.percent_sel.percent_values)

        if current_selection_id != 0:
            current_percent = state_infos.exportations[self.exportation_index][1]
        else:
            current_percent = None
        self.percent_sel.draw(screen, current_percent)
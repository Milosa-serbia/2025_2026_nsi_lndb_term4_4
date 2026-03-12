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
    """Dessine un rect arrondi avec transparence optionnelle."""
    if alpha < 255:
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(tmp, (*color, alpha), tmp.get_rect(), border_radius=radius)
        surface.blit(tmp, rect.topleft)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_border_rect(surface, color, rect, width=1, radius=8):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ============================================================
#  BOUTON PRINCIPAL (menu 1)
# ============================================================
class Button:
    def __init__(self, x, y, width, height, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click
        self._hover_t = 0.0   # animation

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, text, active=False):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)

        # animation douce
        target = 1.0 if hovered else 0.0
        self._hover_t += (target - self._hover_t) * 0.25

        # couleurs interpolées
        if active:
            bg = lerp_color(C_ACCENT, (80, 210, 255), self._hover_t)
            border = C_ACCENT
            txt_color = C_BG
        else:
            bg = lerp_color(C_SURFACE2, C_SURFACE, self._hover_t)
            border = lerp_color(C_BORDER, C_ACCENT, self._hover_t)
            txt_color = lerp_color(C_TEXT_DIM, C_TEXT, self._hover_t)

        # fond
        draw_rounded_rect(screen, bg, self.rect, radius=6)
        draw_border_rect(screen, border, self.rect, width=1, radius=6)

        # icône de chevron à droite (▾) pour les boutons d'export
        label_x = self.rect.x + 12
        surf = self.font.render(text if text else '—', True, txt_color)
        screen.blit(surf, surf.get_rect(midleft=(label_x, self.rect.centery)))

        # petite flèche droite
        arrow_surf = self.font.render('›', True, lerp_color(C_TEXT_DIM, C_ACCENT, self._hover_t))
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
        self._hover_t = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, selected=False):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)
        target = 1.0 if (hovered or selected) else 0.0
        self._hover_t += (target - self._hover_t) * 0.25

        if selected:
            bg = lerp_color(C_SURFACE2, C_ACCENT, 0.25)
            txt_color = C_ACCENT
        else:
            bg = lerp_color(C_SURFACE, C_SURFACE2, self._hover_t)
            txt_color = lerp_color(C_TEXT_DIM, C_TEXT, self._hover_t)

        draw_rounded_rect(screen, bg, self.rect, radius=4)
        if hovered or selected:
            pygame.draw.line(screen, C_ACCENT, self.rect.topleft, self.rect.bottomleft, 2)

        surf = self.font.render(self.text, True, txt_color)
        screen.blit(surf, surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery)))


# ============================================================
#  BOUTON TOGGLE (frontières / confinement)
# ============================================================
class ToggleButton:
    def __init__(self, x, y, width, height, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click
        self._hover_t = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen, active):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)
        target = 1.0 if hovered else 0.0
        self._hover_t += (target - self._hover_t) * 0.25

        if active:
            bg = lerp_color((30, 60, 40), (40, 90, 55), self._hover_t)
            border = C_ACCENT2
            dot_color = C_ACCENT2
            label = 'ACTIF'
            txt_color = C_ACCENT2
        else:
            bg = lerp_color(C_SURFACE, C_SURFACE2, self._hover_t)
            border = lerp_color(C_BORDER, C_TEXT_DIM, self._hover_t)
            dot_color = C_TEXT_DIM
            label = 'INACTIF'
            txt_color = C_TEXT_DIM

        draw_rounded_rect(screen, bg, self.rect, radius=6)
        draw_border_rect(screen, border, self.rect, width=1, radius=6)

        # toggle pill
        pill_w, pill_h = 36, 18
        pill_x = self.rect.x + 10
        pill_y = self.rect.centery - pill_h // 2
        pill_rect = pygame.Rect(pill_x, pill_y, pill_w, pill_h)
        draw_rounded_rect(screen, bg, pill_rect, radius=9)
        draw_border_rect(screen, border, pill_rect, width=1, radius=9)
        dot_cx = pill_x + (pill_w - 10) if active else pill_x + 10
        pygame.draw.circle(screen, dot_color, (dot_cx, pill_y + pill_h // 2), 7)

        txt = self.font.render(label, True, txt_color)
        screen.blit(txt, txt.get_rect(midleft=(pill_x + pill_w + 8, self.rect.centery)))


# ============================================================
#  SCROLLABLE LIST PANEL (menu 2 — remplace les 3 colonnes)
# ============================================================
class ScrollablePanel:
    """Panneau avec liste scrollable pour choisir un état destinataire."""
    def __init__(self, x, y, width, height, font, items, on_select):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.items = items     # liste de (id, name)
        self.on_select = on_select
        self.scroll_y = 0
        self.item_h = 30
        self.max_scroll = max(0, len(items) * self.item_h - (height - 10))
        self._hover_idx = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - event.y * 20))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.rect.collidepoint(mx, my):
                rel_y = my - self.rect.y + self.scroll_y - 5
                idx = rel_y // self.item_h
                if 0 <= idx < len(self.items):
                    self.on_select(self.items[idx][0])

    def draw(self, screen, selected_id=None):
        # fond
        draw_rounded_rect(screen, C_PANEL, self.rect, radius=8)
        draw_border_rect(screen, C_BORDER, self.rect, width=1, radius=8)

        # clip
        clip = screen.get_clip()
        screen.set_clip(self.rect.inflate(-2, -2))

        mx, my = pygame.mouse.get_pos()
        for i, (sid, sname) in enumerate(self.items):
            iy = self.rect.y + 5 + i * self.item_h - self.scroll_y
            if iy + self.item_h < self.rect.y or iy > self.rect.bottom:
                continue
            item_rect = pygame.Rect(self.rect.x + 4, iy, self.rect.width - 8, self.item_h - 2)
            hovered = item_rect.collidepoint(mx, my)
            is_sel = (sid == selected_id)

            if is_sel:
                draw_rounded_rect(screen, lerp_color(C_SURFACE2, C_ACCENT, 0.2), item_rect, radius=4)
                pygame.draw.line(screen, C_ACCENT, item_rect.topleft, item_rect.bottomleft, 2)
                txt_c = C_ACCENT
            elif hovered:
                draw_rounded_rect(screen, C_SURFACE2, item_rect, radius=4)
                txt_c = C_TEXT
            else:
                txt_c = C_TEXT_DIM

            surf = self.font.render(sname, True, txt_c)
            screen.blit(surf, surf.get_rect(midleft=(item_rect.x + 10, item_rect.centery)))

        screen.set_clip(clip)

        # scrollbar
        total_h = len(self.items) * self.item_h
        if total_h > self.rect.height:
            bar_h = max(30, int(self.rect.height * self.rect.height / total_h))
            bar_y = self.rect.y + int(self.scroll_y * (self.rect.height - bar_h) / self.max_scroll) if self.max_scroll > 0 else self.rect.y
            bar_rect = pygame.Rect(self.rect.right - 6, bar_y, 4, bar_h)
            draw_rounded_rect(screen, C_BORDER, bar_rect, radius=2)


# ============================================================
#  PERCENT SELECTOR (rangée de boutons %)
# ============================================================
class PercentSelector:
    def __init__(self, x, y, width, font, on_select):
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.on_select = on_select
        self.percents = list(range(0, 110, 10))
        self.btn_w = (width - (len(self.percents) - 1) * 4) // len(self.percents)
        self._hover_t = [0.0] * len(self.percents)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, p in enumerate(self.percents):
                r = pygame.Rect(self.x + i * (self.btn_w + 4), self.y, self.btn_w, 30)
                if r.collidepoint(event.pos):
                    self.on_select(p)

    def draw(self, screen, current_val):
        mx, my = pygame.mouse.get_pos()
        for i, p in enumerate(self.percents):
            r = pygame.Rect(self.x + i * (self.btn_w + 4), self.y, self.btn_w, 30)
            is_sel = (current_val is not None and int(current_val * 100) == p)
            hovered = r.collidepoint(mx, my)

            target = 1.0 if (hovered or is_sel) else 0.0
            self._hover_t[i] += (target - self._hover_t[i]) * 0.25

            if is_sel:
                bg = C_ACCENT
                txt_c = C_BG
            else:
                bg = lerp_color(C_SURFACE, C_SURFACE2, self._hover_t[i])
                txt_c = lerp_color(C_TEXT_DIM, C_TEXT, self._hover_t[i])

            draw_rounded_rect(screen, bg, r, radius=4)
            draw_border_rect(screen, lerp_color(C_BORDER, C_ACCENT, self._hover_t[i]), r, width=1, radius=4)
            surf = self.font.render(f'{p}', True, txt_c)
            screen.blit(surf, surf.get_rect(center=r.center))


# ============================================================
#  HELPERS DESSIN UI
# ============================================================
def draw_label(screen, font, text, x, y, color=C_TEXT_DIM):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return surf.get_height()


def draw_stat_row(screen, font, label, value, x, y, value_color=C_TEXT):
    lbl = font.render(label, True, C_TEXT_DIM)
    val = font.render(str(value), True, value_color)
    screen.blit(lbl, (x, y))
    screen.blit(val, (x + lbl.get_width() + 6, y))


def draw_section_header(screen, font, text, x, y, w):
    surf = font.render(text.upper(), True, C_ACCENT)
    screen.blit(surf, (x, y))
    pygame.draw.line(screen, C_BORDER, (x, y + surf.get_height() + 3), (x + w, y + surf.get_height() + 3), 1)
    return surf.get_height() + 8


def draw_progress_bar(screen, x, y, w, h, value, max_val, color_fill, bg_color=C_SURFACE):
    bar_rect = pygame.Rect(x, y, w, h)
    draw_rounded_rect(screen, bg_color, bar_rect, radius=h // 2)
    fill = max(0, min(w, int(w * value / max_val)))
    if fill > 0:
        fill_rect = pygame.Rect(x, y, fill, h)
        draw_rounded_rect(screen, color_fill, fill_rect, radius=h // 2)
    draw_border_rect(screen, C_BORDER, bar_rect, width=1, radius=h // 2)


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

        # Menu 2 (panneau droit — dropdown/liste)
        self.menu2_open = False
        self.PANEL2_W   = 380
        self.menu2_rect = pygame.Rect(380, 15, self.PANEL2_W, self.PANEL_H)
        self.exportation_index = None

        # Construire la liste des états pour le menu 2
        self.state_list = [(0, '— Aucun —')] + [(id, infos[id].name) for id in range(101, 147)]

        # Scrollable list dans le menu 2
        self.state_scroll = ScrollablePanel(
            self.menu2_rect.x + 10, self.menu2_rect.y + 90,
            self.PANEL2_W - 20, 500,
            self.font,
            self.state_list,
            on_select=lambda sid: self.change_exportation_id(infos, sid)
        )

        # PercentSelector
        self.percent_sel = PercentSelector(
            self.menu2_rect.x + 10, self.menu2_rect.y + 620,
            self.PANEL2_W - 20, self.font_sm,
            on_select=lambda p: self.change_exportations_percent(infos, p)
        )

        # Boutons d'export (4 slots)
        bx = self.menu_rect.x + 14
        self.exportation_buttons = [
            Button(bx,       self.menu_rect.y + 355, 155, 32, self.font, lambda i=0: self.open_menu2(i)),
            Button(bx + 163, self.menu_rect.y + 355, 155, 32, self.font, lambda i=1: self.open_menu2(i)),
            Button(bx,       self.menu_rect.y + 395, 155, 32, self.font, lambda i=2: self.open_menu2(i)),
            Button(bx + 163, self.menu_rect.y + 395, 155, 32, self.font, lambda i=3: self.open_menu2(i)),
        ]

        # Boutons toggle
        self.border_button = ToggleButton(
            self.menu_rect.x + 14, self.menu_rect.y + 460, 300, 34, self.font,
            lambda: self.change_border_statue(infos, self.closed_border_states)
        )
        self.lockdown_button = ToggleButton(
            self.menu_rect.x + 14, self.menu_rect.y + 504, 300, 34, self.font,
            lambda: self.change_lockdown_statue(infos, self.lockdowned_states)
        )

        # Images
        self.lockdown_image = pygame.image.load("Enter.png").convert_alpha()
        self.lockdown_image = pygame.transform.scale(self.lockdown_image, (22, 22))
        self.closed_border_image = pygame.image.load("Locked.png").convert_alpha()
        self.closed_border_image = pygame.transform.scale(self.closed_border_image, (22, 22))
        self.closed_border_and_lockdown_image = pygame.image.load("Power.png").convert_alpha()
        self.closed_border_and_lockdown_image = pygame.transform.scale(self.closed_border_and_lockdown_image, (22, 22))
        self.scientist_image = pygame.image.load("Scientist.png").convert_alpha()
        self.scientist_image = pygame.transform.scale(self.scientist_image, (48, 48))

        # surface de vignette (overlay noir sur les bords)
        screen = pygame.display.get_surface()
        self._vignette = self._make_vignette(screen.get_width(), screen.get_height())

    # ------------------------------------------------------------------
    def _make_vignette(self, w, h):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for i in range(60):
            alpha = int(120 * (1 - i / 60) ** 2)
            pygame.draw.rect(surf, (0, 0, 0, alpha), (i, i, w - 2*i, h - 2*i), 1)
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
        if old_export_id != 0:
            try:
                infos[old_export_id].importations.remove(current_state.name)
            except ValueError:
                pass
        current_state.exportations[self.exportation_index][0] = new_export_id
        current_state.exportations[self.exportation_index][1] = 0
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
    #  INPUT
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
    #  DESSIN
    # ------------------------------------------------------------------
    def draw(self, screen, infos, vaccine_progression):
        # vignette de bords
        screen.blit(self._vignette, (0, 0))

        # ---- Barre vaccin (haut droite) ----
        self._draw_vaccine_bar(screen, vaccine_progression)

        # ---- Icônes d'état sur la carte ----
        self._draw_state_icons(screen, infos)

        # ---- Menu principal ----
        if self.menu_open and self.px_id is not None:
            self._draw_main_panel(screen, infos)

        if self.menu2_open and self.menu_open:
            self._draw_menu2(screen, infos)

    # ------------------------------------------------------------------
    def _draw_vaccine_bar(self, screen, vaccine_progression):
        bx, by = 1050, 14
        bw, bh = 380, 46

        # fond du panneau vaccin
        panel = pygame.Rect(bx - 10, by - 4, bw + 20, bh + 8)
        draw_rounded_rect(screen, C_PANEL, panel, radius=10, alpha=210)
        draw_border_rect(screen, C_BORDER, panel, width=1, radius=10)

        # icône
        screen.blit(self.scientist_image, (bx - 8, by - 2))

        # label
        label_surf = self.font_sm.render('VACCIN EN COURS :', True, C_TEXT_DIM)
        screen.blit(label_surf, (bx + 46, by + 2))

        # barre
        bar_rect = pygame.Rect(bx + 46, by + 20, bw - 56, 14)
        draw_rounded_rect(screen, C_SURFACE, bar_rect, radius=7)
        fill_w = int((bw - 56) * vaccine_progression / 100)
        if fill_w > 0:
            # gradient simulé par deux rects
            fill_rect = pygame.Rect(bx + 46, by + 20, fill_w, 14)
            draw_rounded_rect(screen, C_ACCENT, fill_rect, radius=7)
        draw_border_rect(screen, C_BORDER, bar_rect, width=1, radius=7)

        # pourcentage — à l'intérieur du rect, aligné à droite
        pct_surf = self.font_sm.render(f'{int(vaccine_progression)}%', True, C_WHITE)
        screen.blit(pct_surf, pct_surf.get_rect(midright=(bar_rect.right - 140, by + 10)))

    # ------------------------------------------------------------------
    def _draw_state_icons(self, screen, infos):
        cb_copy = self.closed_border_states.copy()
        for id_ in self.lockdowned_states:
            pos = infos[id_].ui_pos
            if not pos:
                continue
            if id_ not in cb_copy:
                screen.blit(self.lockdown_image, (pos[0] - 4, pos[1] - 4))
            else:
                cb_copy.remove(id_)
                screen.blit(self.closed_border_and_lockdown_image, (pos[0] - 4, pos[1] - 4))
        for id_ in cb_copy:
            pos = infos[id_].ui_pos
            if pos:
                screen.blit(self.closed_border_image, (pos[0] - 4, pos[1] - 4))

    # ------------------------------------------------------------------
    def _draw_main_panel(self, screen, infos):
        id_infos = infos[self.px_id]
        p = self.menu_rect

        # ombre + fond
        shadow = p.inflate(8, 8).move(4, 4)
        draw_rounded_rect(screen, (0, 0, 0), shadow, radius=14, alpha=120)
        draw_rounded_rect(screen, C_PANEL, p, radius=12, alpha=245)
        draw_border_rect(screen, C_BORDER, p, width=1, radius=12)

        # ---- En-tête ----
        header_rect = pygame.Rect(p.x, p.y, p.width, 68)
        draw_rounded_rect(screen, C_SURFACE2, header_rect, radius=12)
        pygame.draw.rect(screen, C_SURFACE2, pygame.Rect(p.x, p.y + 40, p.width, 28))

        accent_bar = pygame.Rect(p.x, p.y, 4, 68)
        draw_rounded_rect(screen, C_ACCENT, accent_bar, radius=2)

        title = self.font_lg.render(id_infos.name, True, C_WHITE)
        screen.blit(title, (p.x + 18, p.y + 12))
        sub = self.font_sm.render(f'ID ÉTAT  ·  #{self.px_id}', True, C_TEXT_DIM)
        screen.blit(sub, (p.x + 18, p.y + 48))

        # Layout constants — on exploite toute la hauteur du panneau (820px - 68 header = 752px dispo)
        PAD   = 18   # marge horizontale
        SEC   = 14   # espace avant chaque section header
        AFTER = 10   # espace après chaque section header
        ROW   = 24   # hauteur d'une ligne de stat
        BTN_H = 36   # hauteur des boutons export / toggle

        y = p.y + 78  # démarre juste sous le header

        # ---- Section Population ----
        y += SEC
        y += draw_section_header(screen, self.font_sm, '  Population', p.x + PAD, y, p.width - PAD*2)
        y += AFTER

        total = id_infos.population
        alive = int(id_infos.alive_population)
        dead  = total - alive
        pct_alive = alive / total if total else 0

        # barre pop (large, bien visible)
        draw_progress_bar(screen, p.x + PAD, y, p.width - PAD*2, 12, alive, total, C_ACCENT2)
        y += 20

        # deux stats côte à côte
        draw_stat_row(screen, self.font_sm, 'Vivants :', f'{alive:,}', p.x + PAD, y, C_ACCENT2)
        draw_stat_row(screen, self.font_sm, 'Morts / inf. :', f'{dead:,}', p.x + PAD + 170, y, C_DANGER)
        y += ROW
        pct_surf = self.font_sm.render(f'{pct_alive*100:.1f}% de la population initiale survit', True, C_TEXT_DIM)
        screen.blit(pct_surf, (p.x + PAD, y))
        y += ROW + 4

        # ---- Section Santé & Ressources ----
        y += SEC
        y += draw_section_header(screen, self.font_sm, '  Santé & Ressources', p.x + PAD, y, p.width - PAD*2)
        y += AFTER

        draw_stat_row(screen, self.font_sm, "Obésité :", f"{id_infos.obesity_rate*100:.1f}%", p.x + PAD, y)
        draw_stat_row(screen, self.font_sm, 'Prod. végétale :', f'{int(id_infos.vegetable_production):,}', p.x + PAD + 130, y)
        y += ROW + 4

        # barre réserves alimentaires
        food_max = max(id_infos.population * 100, id_infos.food_ressources + 1)
        food_color = C_ACCENT2 if id_infos.food_ressources > id_infos.population * 20 else C_WARNING if id_infos.food_ressources > 0 else C_DANGER
        draw_progress_bar(screen, p.x + PAD, y, p.width - PAD*2, 12, id_infos.food_ressources, food_max, food_color)
        y += 20
        draw_stat_row(screen, self.font_sm, 'Réserves alim. :', f'{int(id_infos.food_ressources):,}', p.x + PAD, y, food_color)
        y += ROW + 4

        # ---- Section Exportations ----
        y += SEC
        y += draw_section_header(screen, self.font_sm, '  Exportations (4 slots)', p.x + PAD, y, p.width - PAD*2)
        y += AFTER

        labels = ['Slot A', 'Slot B', 'Slot C', 'Slot D']
        slot_w = (p.width - PAD*2 - 10) // 2  # largeur d'un slot
        slot_x = [p.x + PAD, p.x + PAD + slot_w + 10]

        for i, btn in enumerate(self.exportation_buttons):
            row_y = y + (i // 2) * (14 + BTN_H + 8)  # 2 lignes de 2 slots
            col_x = slot_x[i % 2]

            export_id   = id_infos.exportations[i][0]
            export_name = infos[export_id].name if export_id != 0 else ''
            pct         = int(id_infos.exportations[i][1] * 100)

            # label slot BIEN au-dessus du bouton
            lbl_text = f'{labels[i]}  —  {pct}%' if export_id != 0 else labels[i]
            lbl_surf = self.font_sm.render(lbl_text, True, C_TEXT_DIM)
            screen.blit(lbl_surf, (col_x, row_y))

            # bouton positionné SOUS le label
            btn.rect.x = col_x
            btn.rect.y = row_y + 16
            btn.rect.width  = slot_w
            btn.rect.height = BTN_H
            is_open = self.menu2_open and self.exportation_index == i
            btn.draw(screen, export_name, active=is_open)

        # avance y après les 2 lignes de slots
        y += 2 * (14 + BTN_H + 8) + 4

        # ---- Section Mesures sanitaires ----
        y += SEC
        y += draw_section_header(screen, self.font_sm, '  Mesures sanitaires', p.x + PAD, y, p.width - PAD*2)
        y += AFTER

        # Frontières
        cb_lbl = self.font_sm.render('Fermer les frontières', True, C_TEXT_DIM)
        screen.blit(cb_lbl, (p.x + PAD, y))
        y += 16
        self.border_button.rect.x = p.x + PAD
        self.border_button.rect.y = y
        self.border_button.rect.width = p.width - PAD*2
        self.border_button.rect.height = BTN_H
        self.border_button.draw(screen, id_infos.closed_border)
        y += BTN_H + 12

        # Confinement
        ld_lbl = self.font_sm.render('Confinement', True, C_TEXT_DIM)
        screen.blit(ld_lbl, (p.x + PAD, y))
        y += 16
        self.lockdown_button.rect.x = p.x + PAD
        self.lockdown_button.rect.y = y
        self.lockdown_button.rect.width = p.width - PAD*2
        self.lockdown_button.rect.height = BTN_H
        self.lockdown_button.draw(screen, id_infos.lockdown)
        y += BTN_H + 8

        # ---- Section Importations ----
        y += SEC
        y += draw_section_header(screen, self.font_sm, '  Importations reçues', p.x + PAD, y, p.width - PAD*2)
        y += AFTER - 5

        if id_infos.importations:
            for imp in id_infos.importations:
                chip_rect = pygame.Rect(p.x + PAD, y, p.width - PAD*2, ROW - 2)
                draw_rounded_rect(screen, C_SURFACE2, chip_rect, radius=4)
                pygame.draw.line(screen, C_ACCENT2, chip_rect.topleft, chip_rect.bottomleft, 2)
                chip_surf = self.font_sm.render(f'← {imp}', True, C_ACCENT2)
                screen.blit(chip_surf, chip_surf.get_rect(midleft=(chip_rect.x + 10, chip_rect.centery)))
                y += ROW + 4
        else:
            none_surf = self.font_sm.render('Aucune importation active', True, C_TEXT_DIM)
            screen.blit(none_surf, (p.x + PAD, y))

    # ------------------------------------------------------------------
    def _draw_menu2(self, screen, infos):
        if self.px_id is None or self.exportation_index is None:
            return
        p = self.menu2_rect
        id_infos = infos[self.px_id]
        labels = ['Slot A', 'Slot B', 'Slot C', 'Slot D']

        # fond
        shadow = p.inflate(8, 8).move(4, 4)
        draw_rounded_rect(screen, (0, 0, 0), shadow, radius=14, alpha=100)
        draw_rounded_rect(screen, C_PANEL, p, radius=12, alpha=245)
        draw_border_rect(screen, C_BORDER, p, width=1, radius=12)

        # en-tête
        header_rect = pygame.Rect(p.x, p.y, p.width, 68)
        draw_rounded_rect(screen, C_SURFACE2, header_rect, radius=12)
        pygame.draw.rect(screen, C_SURFACE2, pygame.Rect(p.x, p.y + 40, p.width, 28))
        accent_bar = pygame.Rect(p.x, p.y, 4, 68)
        draw_rounded_rect(screen, (99, 235, 167), accent_bar, radius=2)

        title = self.font_lg.render(f'Exportation · {labels[self.exportation_index]}', True, C_WHITE)
        screen.blit(title, (p.x + 16, p.y + 12))
        sub = self.font_sm.render(f'Destination depuis {id_infos.name}', True, C_TEXT_DIM)
        screen.blit(sub, (p.x + 16, p.y + 48))

        # Séparateur liste
        y = p.y + 78
        lbl_list = self.font_sm.render('ÉTAT DESTINATAIRE', True, C_TEXT_DIM)
        screen.blit(lbl_list, (p.x + 14, y))
        y += 20

        # scrollable list
        self.state_scroll.rect.y = y
        self.state_scroll.rect.x = p.x + 10
        self.state_scroll.rect.width = p.width - 20
        self.state_scroll.rect.height = 480
        current_sel = id_infos.exportations[self.exportation_index][0]
        self.state_scroll.draw(screen, selected_id=current_sel)

        y = self.state_scroll.rect.bottom + 16

        # pourcentage
        lbl_pct = self.font_sm.render('POURCENTAGE DE PRODUCTION EXPORTÉ (%)', True, C_TEXT_DIM)
        screen.blit(lbl_pct, (p.x + 14, y))
        y += 20

        self.percent_sel.x = p.x + 10
        self.percent_sel.y = y
        self.percent_sel.btn_w = (p.width - 20 - (len(self.percent_sel.percents) - 1) * 4) // len(self.percent_sel.percents)
        current_pct = id_infos.exportations[self.exportation_index][1] if current_sel != 0 else None
        self.percent_sel.draw(screen, current_pct)
    
            
            
            
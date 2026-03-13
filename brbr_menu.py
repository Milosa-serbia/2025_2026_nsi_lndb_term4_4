import pygame
import math
import random
import sys


# ============================================================
#  PALETTE — identique à brbr_ui.py
# ============================================================
C_BG       = (12,  14,  20)
C_PANEL    = (18,  22,  32)
C_SURFACE  = (26,  32,  46)
C_SURFACE2 = (32,  40,  58)
C_BORDER   = (48,  60,  90)
C_ACCENT   = (56, 189, 248)
C_ACCENT2  = (99, 235, 167)
C_DANGER   = (248,  82,  82)
C_WARNING  = (251, 189,  35)
C_TEXT     = (220, 228, 245)
C_TEXT_DIM = (100, 115, 150)
C_WHITE    = (255, 255, 255)


# ============================================================
#  HELPERS DE DESSIN (copiés depuis brbr_ui pour autonomie)
# ============================================================
def draw_rounded_rect(surface, color, rect, radius=8, alpha=255) :
    if alpha < 255 :
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(tmp, (*color, alpha), tmp.get_rect(), border_radius=radius)
        surface.blit(tmp, rect.topleft)
    else :
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_border_rect(surface, color, rect, width=1, radius=8) :
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)


def lerp_color(color_a, color_b, t) :
    """Interpolation linéaire entre deux couleurs RGB selon t (entre 0.0 et 1.0)."""
    r = int(color_a[0] + (color_b[0] - color_a[0]) * t)
    g = int(color_a[1] + (color_b[1] - color_a[1]) * t)
    b = int(color_a[2] + (color_b[2] - color_a[2]) * t)
    return (r, g, b)


# ============================================================
#  PARTICULES DE FOND
# ============================================================
class Particle :
    def __init__(self, screen_width, screen_height) :
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.respawn(initial=True)

    def respawn(self, initial=False) :
        self.x = random.uniform(0, self.screen_width)
        # au démarrage on place les particules n'importe où,
        # sinon elles réapparaissent en bas de l'écran
        if initial :
            self.y = random.uniform(0, self.screen_height)
        else :
            self.y = self.screen_height + 2
        self.speed = random.uniform(0.2, 0.8)
        self.radius = random.uniform(0.5, 2.0)
        self.alpha = random.randint(30, 120)
        # couleur aléatoire entre cyan et vert mint
        color_blend = random.random()
        self.color = lerp_color(C_ACCENT, C_ACCENT2, color_blend)

    def update(self) :
        self.y -= self.speed
        if self.y < -5 :
            self.respawn()

    def draw(self, surface) :
        if self.radius < 1 :
            return
        # on dessine sur une surface temporaire pour gérer la transparence
        tmp_size = int(self.radius * 2 + 2)
        tmp = pygame.Surface((tmp_size, tmp_size), pygame.SRCALPHA)
        center = (int(self.radius + 1), int(self.radius + 1))
        pygame.draw.circle(tmp, (*self.color, self.alpha), center, int(self.radius))
        surface.blit(tmp, (int(self.x - self.radius), int(self.y - self.radius)))


# ============================================================
#  LIGNES DE SCAN (effet visuel de fond)
# ============================================================
def draw_scanlines(surface, screen_width, screen_height) :
    """Dessine des lignes horizontales très légères pour un effet CRT."""
    scanline_surf = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    y = 0
    while y < screen_height :
        pygame.draw.line(scanline_surf, (0, 0, 0, 18), (0, y), (screen_width, y))
        y += 4
    surface.blit(scanline_surf, (0, 0))


# ============================================================
#  GRILLE DE FOND ANIMÉE
# ============================================================
class BackgroundGrid :
    def __init__(self, screen_width, screen_height) :
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_offset = 0.0
        self.cell_size = 60

    def update(self) :
        self.scroll_offset = (self.scroll_offset + 0.3) % self.cell_size

    def draw(self, surface) :
        grid_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        grid_color = (*C_BORDER, 35)

        # lignes verticales
        x = -self.cell_size + (self.scroll_offset % self.cell_size)
        while x < self.screen_width :
            pygame.draw.line(grid_surf, grid_color, (int(x), 0), (int(x), self.screen_height))
            x += self.cell_size

        # lignes horizontales
        y = -self.cell_size + (self.scroll_offset % self.cell_size)
        while y < self.screen_height :
            pygame.draw.line(grid_surf, grid_color, (0, int(y)), (self.screen_width, int(y)))
            y += self.cell_size

        surface.blit(grid_surf, (0, 0))


# ============================================================
#  BOUTON DU MENU PRINCIPAL
# ============================================================
class MenuButton :
    BUTTON_HEIGHT = 52

    def __init__(self, label, sublabel, accent_color, on_click) :
        self.label = label
        self.sublabel = sublabel
        self.accent_color = accent_color
        self.on_click = on_click
        self.rect = pygame.Rect(0, 0, 0, self.BUTTON_HEIGHT)  # position définie dans draw()
        self.hover_animation = 0.0  # valeur entre 0.0 et 1.0 pour l'animation de survol
        self.click_flash = 0.0      # animation rapide au clic

    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            if self.rect.collidepoint(event.pos) :
                self.click_flash = 1.0
                if self.on_click is not None :
                    self.on_click()

    def update(self) :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) :
            hover_target = 1.0
        else :
            hover_target = 0.0
        self.hover_animation += (hover_target - self.hover_animation) * 0.15
        if self.click_flash > 0 :
            self.click_flash -= 0.1

    def draw(self, screen, font_label, font_sublabel, x, y, width) :
        self.rect = pygame.Rect(x, y, width, self.BUTTON_HEIGHT)
        t = self.hover_animation

        # fond du bouton
        bg_color = lerp_color(C_SURFACE, C_SURFACE2, t)
        draw_rounded_rect(screen, bg_color, self.rect, radius=8)

        # bordure qui s'allume progressivement en survol
        border_color = lerp_color(C_BORDER, self.accent_color, t)
        draw_border_rect(screen, border_color, self.rect, width=1, radius=8)

        # barre accent sur la gauche — grandit vers le haut et le bas en survol
        bar_height = int(10 + (self.BUTTON_HEIGHT - 10) * t)
        bar_y = y + (self.BUTTON_HEIGHT - bar_height) // 2
        bar_rect = pygame.Rect(x, bar_y, 4, bar_height)
        draw_rounded_rect(screen, self.accent_color, bar_rect, radius=2)

        # lueur colorée derrière le bouton, visible uniquement en survol
        if t > 0.05 :
            glow_alpha = int(t * 30)
            glow_surf = pygame.Surface((width, self.BUTTON_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.accent_color, glow_alpha), glow_surf.get_rect(), border_radius=8)
            screen.blit(glow_surf, (x, y))

        # label principal
        text_color = lerp_color(C_TEXT_DIM, C_WHITE, t)
        label_surf = font_label.render(self.label, True, text_color)
        label_pos = label_surf.get_rect(midleft=(x + 20, y + self.BUTTON_HEIGHT // 2 - 6))
        screen.blit(label_surf, label_pos)

        # sous-label
        sub_color_mid = lerp_color(C_TEXT_DIM, self.accent_color, 0.5)
        sub_color = lerp_color(C_TEXT_DIM, sub_color_mid, t)
        sub_surf = font_sublabel.render(self.sublabel, True, sub_color)
        sub_pos = sub_surf.get_rect(midleft=(x + 22, y + self.BUTTON_HEIGHT // 2 + 12))
        screen.blit(sub_surf, sub_pos)

        # flèche à droite
        arrow_color = lerp_color(C_BORDER, self.accent_color, t)
        arrow_surf = font_label.render('›', True, arrow_color)
        arrow_pos = arrow_surf.get_rect(midright=(x + width - 16, y + self.BUTTON_HEIGHT // 2))
        screen.blit(arrow_surf, arrow_pos)


# ============================================================
#  PAGE DES RÈGLES
# ============================================================
class RulesPage :
    # Contenu des sections : (titre, couleur, [lignes de texte])
    RULES_TEXT = [
        ("L'INFECTION", C_ACCENT, [
            "Un premier foyer apparaît aléatoirement aux États-Unis.",
            "La maladie se propage de pixel en pixel par contact direct,",
            "mais aussi par voie aérienne sur de longues distances.",
            "Les pixels infectés peuvent mourir ou transmettre la maladie.",
        ]),
        ("LE VACCIN", C_ACCENT2, [
            "Un vaccin est en cours de développement — sa progression",
            "est affichée en haut à droite de l'écran.",
            "Lorsqu'il atteint 100%, la partie se termine et votre score",
            "est calculé en fonction de la population encore en vie.",
        ]),
        ("LES ÉTATS", C_WARNING, [
            "Cliquez sur un état de la carte pour ouvrir son panneau.",
            "Vous pouvez y consulter sa population, ses réserves",
            "alimentaires, et configurer ses exportations vers d'autres états.",
        ]),
        ("LES MESURES SANITAIRES", C_DANGER, [
            "Fermer les frontières : ralentit la propagation entre états",
            "mais réduit la production alimentaire de l'état.",
            "Confinement : stoppe la transmission aérienne dans l'état",
            "mais réduit également la production alimentaire.",
            "Maximum 4 états simultanément pour chaque mesure.",
        ]),
        ("LA FAMINE", (220, 20, 10), [
            "Chaque état consomme de la nourriture en fonction de sa",
            "population et de son taux d'obésité.",
            "Si les réserves tombent à zéro, des habitants commencent",
            "à mourir de faim. Gérez les exportations pour équilibrer",
            "la nourriture entre les états riches et les états déficitaires.",
        ]),
    ]

    def __init__(self, screen_width, screen_height) :
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        self.scroll_y = 0.0       # position de scroll actuelle (lissée)
        self.scroll_target = 0.0  # position de scroll cible (mise à jour par la molette)

        self.font_section_title = pygame.font.Font(None, 30)
        self.font_body          = pygame.font.Font(None, 22)
        self.font_back_button   = pygame.font.Font(None, 26)

        # bouton "Retour au menu", centré en bas de l'écran
        btn_width  = 240
        btn_height = 42
        self.back_button_rect = pygame.Rect(
            screen_width // 2 - btn_width // 2,
            screen_height - 65,
            btn_width,
            btn_height
        )
        self.back_button_hover = 0.0  # animation de survol du bouton retour

    def handle_event(self, event) :
        if event.type == pygame.MOUSEWHEEL :
            self.scroll_target = max(0, self.scroll_target - event.y * 30)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            if self.back_button_rect.collidepoint(event.pos) :
                self.is_open = False

    def update(self) :
        # scroll fluide : on se rapproche de la cible à chaque frame
        self.scroll_y += (self.scroll_target - self.scroll_y) * 0.15

        # animation de survol du bouton retour
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.back_button_rect.collidepoint(mouse_x, mouse_y) :
            back_hover_target = 1.0
        else :
            back_hover_target = 0.0
        self.back_button_hover += (back_hover_target - self.back_button_hover) * 0.15

    def draw(self, screen) :
        screen.fill(C_BG)
        draw_scanlines(screen, self.screen_width, self.screen_height)

        panel_width = 820
        panel_x = self.screen_width // 2 - panel_width // 2
        panel_y = 40

        # titre de la page
        title_font = pygame.font.Font(None, 56)
        title_surf = title_font.render('RÈGLES DU JEU', True, C_ACCENT)
        screen.blit(title_surf, title_surf.get_rect(centerx=self.screen_width // 2, y=panel_y))

        # ligne décorative sous le titre (grise + petit segment cyan à gauche)
        separator_y = panel_y + title_surf.get_height() + 8
        pygame.draw.line(screen, C_BORDER, (panel_x, separator_y), (panel_x + panel_width, separator_y), 1)
        accent_segment_width = 80
        pygame.draw.line(screen, C_ACCENT, (panel_x, separator_y), (panel_x + accent_segment_width, separator_y), 2)

        # zone de contenu scrollable
        content_top    = separator_y + 20
        content_height = self.screen_height - content_top - 100
        content_area   = pygame.Rect(panel_x, content_top, panel_width, content_height)

        old_clip = screen.get_clip()
        screen.set_clip(content_area)

        current_y = content_area.y + 10 - int(self.scroll_y)

        for section_title, section_color, text_lines in self.RULES_TEXT :
            section_height = 28 + len(text_lines) * 22 + 16
            section_rect = pygame.Rect(panel_x, current_y, panel_width, section_height)
            draw_rounded_rect(screen, C_PANEL, section_rect, radius=8)
            draw_border_rect(screen, C_BORDER, section_rect, width=1, radius=8)

            # barre colorée à gauche de la section
            left_bar_rect = pygame.Rect(panel_x, current_y, 4, section_height)
            draw_rounded_rect(screen, section_color, left_bar_rect, radius=2)

            # titre de la section
            section_title_surf = self.font_section_title.render(section_title, True, section_color)
            screen.blit(section_title_surf, (panel_x + 18, current_y + 10))
            current_y += 36

            # lignes de texte de la section
            for line_text in text_lines :
                line_surf = self.font_body.render(line_text, True, C_TEXT)
                screen.blit(line_surf, (panel_x + 20, current_y))
                current_y += 22

            current_y += 18  # espace entre les sections

        # calcul du scroll max pour empêcher de défiler trop loin
        total_content_height = current_y - (content_area.y - int(self.scroll_y))
        max_scroll = max(0, total_content_height - content_area.height + int(self.scroll_y))
        self.scroll_target = min(self.scroll_target, max_scroll)

        screen.set_clip(old_clip)

        # scrollbar verticale
        if total_content_height > content_area.height :
            track_rect = pygame.Rect(panel_x + panel_width + 8, content_area.y, 4, content_area.height)
            draw_rounded_rect(screen, C_SURFACE2, track_rect, radius=2)

            scrollbar_height = max(40, int(content_area.height * content_area.height / total_content_height))
            if max_scroll > 0 :
                scrollbar_y = content_area.y + int(self.scroll_y * (content_area.height - scrollbar_height) / max_scroll)
            else :
                scrollbar_y = content_area.y
            scrollbar_rect = pygame.Rect(panel_x + panel_width + 8, scrollbar_y, 4, scrollbar_height)
            draw_rounded_rect(screen, C_ACCENT, scrollbar_rect, radius=2)

        # bouton retour
        t = self.back_button_hover
        back_bg_color     = lerp_color(C_SURFACE, C_SURFACE2, t)
        back_border_color = lerp_color(C_BORDER, C_ACCENT2, t)
        back_text_color   = lerp_color(C_TEXT_DIM, C_WHITE, t)
        draw_rounded_rect(screen, back_bg_color, self.back_button_rect, radius=8)
        draw_border_rect(screen, back_border_color, self.back_button_rect, width=1, radius=8)
        back_label_surf = self.font_back_button.render('‹  Retour au menu', True, back_text_color)
        screen.blit(back_label_surf, back_label_surf.get_rect(center=self.back_button_rect.center))


# ============================================================
#  MENU PRINCIPAL
# ============================================================
class MainMenu :
    GAME_TITLE    = "PATHOGEN"
    GAME_SUBTITLE = "PANDEMIC SIMULATION"

    def __init__(self, screen_width, screen_height) :
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.result = None  # vaut 'play' quand le joueur clique sur Jouer

        # polices
        self.font_title    = pygame.font.Font(None, 110)
        self.font_subtitle = pygame.font.Font(None, 30)
        self.font_label    = pygame.font.Font(None, 30)
        self.font_sublabel = pygame.font.Font(None, 20)
        self.font_version  = pygame.font.Font(None, 20)

        # éléments de fond animés
        self.background_grid = BackgroundGrid(screen_width, screen_height)
        self.particles = []
        for i in range(80) :
            self.particles.append(Particle(screen_width, screen_height))

        # animation du titre (révélation progressive au démarrage)
        self.title_time         = 0.0  # temps qui avance pour la pulsation du halo
        self.title_reveal_timer = 0    # compteur de frames depuis le début

        # page des règles (affichée par-dessus le menu)
        self.rules_page = RulesPage(screen_width, screen_height)

        # position et taille des boutons
        self.button_width    = 400
        self.button_center_x = screen_width // 2 - self.button_width // 2

        self.btn_play = MenuButton(
            label='LANCER LA SIMULATION',
            sublabel='Démarrer une nouvelle partie',
            accent_color=C_ACCENT,
            on_click=self.on_play_clicked
        )
        self.btn_rules = MenuButton(
            label='COMMENT JOUER',
            sublabel='Règles et mécaniques du jeu',
            accent_color=C_ACCENT2,
            on_click=self.on_rules_clicked
        )

    def on_play_clicked(self) :
        self.result = 'play'

    def on_rules_clicked(self) :
        self.rules_page.is_open = True
        self.rules_page.scroll_y = 0
        self.rules_page.scroll_target = 0

    def handle_event(self, event) :
        if self.rules_page.is_open :
            self.rules_page.handle_event(event)
            return
        self.btn_play.handle_event(event)
        self.btn_rules.handle_event(event)

    def update(self) :
        if self.rules_page.is_open :
            self.rules_page.update()
            return

        self.background_grid.update()
        for particle in self.particles :
            particle.update()

        self.title_time += 0.02
        self.title_reveal_timer += 1

    def draw(self, screen) :
        if self.rules_page.is_open :
            self.rules_page.draw(screen)
            return

        # ---- Fond ----
        screen.fill(C_BG)
        self.background_grid.draw(screen)
        for particle in self.particles :
            particle.draw(screen)
        draw_scanlines(screen, self.screen_width, self.screen_height)

        # ---- Vignette (bords assombris) ----
        vignette = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for i in range(80) :
            alpha = int(160 * (1 - i / 80) ** 2)
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (i, i, self.screen_width - 2*i, self.screen_height - 2*i), 1)
        screen.blit(vignette, (0, 0))

        center_x = self.screen_width // 2
        title_y  = self.screen_height // 2 - 180

        # ---- Halo derrière le titre (pulsation animée) ----
        glow_alpha = int(80 + math.sin(self.title_time * 2) * 30)
        title_raw_surf = self.font_title.render(self.GAME_TITLE, True, C_ACCENT)
        glow_surf_width  = title_raw_surf.get_width() + 60
        glow_surf_height = title_raw_surf.get_height() + 30
        glow_surf = pygame.Surface((glow_surf_width, glow_surf_height), pygame.SRCALPHA)
        glow_font = pygame.font.Font(None, 110)
        glow_text_surf = glow_font.render(self.GAME_TITLE, True, (*C_ACCENT, glow_alpha))
        # on superpose le texte du halo plusieurs fois avec de légers décalages pour simuler un flou
        glow_surf.blit(glow_text_surf, (30, 15))
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)] :
            glow_surf.blit(glow_text_surf, (30 + dx, 15 + dy))
        glow_center_y = title_y + title_raw_surf.get_height() // 2
        screen.blit(glow_surf, glow_surf.get_rect(centerx=center_x, centery=glow_center_y))

        # ---- Titre principal ----
        title_color = lerp_color(C_ACCENT, C_WHITE, 0.15)
        title_surf = self.font_title.render(self.GAME_TITLE, True, title_color)
        screen.blit(title_surf, title_surf.get_rect(centerx=center_x, y=title_y))

        # ---- Ligne décorative sous le titre ----
        title_line_width = title_surf.get_width()
        title_line_y     = title_y + title_surf.get_height() + 4
        line_left_x  = center_x - title_line_width // 2
        line_right_x = center_x + title_line_width // 2
        pygame.draw.line(screen, C_BORDER, (line_left_x, title_line_y), (line_right_x, title_line_y), 1)

        # segment cyan animé qui s'étend depuis le centre au démarrage
        accent_progress = min(1.0, self.title_reveal_timer / 40)
        accent_half_width = int((title_line_width // 2) * accent_progress)
        if accent_half_width > 0 :
            pygame.draw.line(
                screen, C_ACCENT,
                (center_x - accent_half_width, title_line_y),
                (center_x + accent_half_width, title_line_y),
                2
            )

        # ---- Sous-titre (apparaît progressivement) ----
        sub_alpha = min(255, max(0, (self.title_reveal_timer - 20) * 8))
        if sub_alpha > 0 :
            sub_surf = self.font_subtitle.render(self.GAME_SUBTITLE, True, (*C_TEXT_DIM, sub_alpha))
            sub_tmp = pygame.Surface(sub_surf.get_size(), pygame.SRCALPHA)
            sub_tmp.blit(sub_surf, (0, 0))
            screen.blit(sub_tmp, sub_tmp.get_rect(centerx=center_x, y=title_line_y + 10))

        # ---- Cadre des boutons ----
        buttons_top_y = self.screen_height // 2 - 20
        panel_rect = pygame.Rect(
            self.button_center_x - 20,
            buttons_top_y - 16,
            self.button_width + 40,
            MenuButton.BUTTON_HEIGHT * 2 + 12 + 32 + 8
        )
        draw_rounded_rect(screen, C_PANEL, panel_rect, radius=12, alpha=200)
        draw_border_rect(screen, C_BORDER, panel_rect, width=1, radius=12)

        # petit label au-dessus des boutons
        menu_label_surf = self.font_sublabel.render('— MENU PRINCIPAL —', True, C_TEXT_DIM)
        screen.blit(menu_label_surf, menu_label_surf.get_rect(centerx=center_x, y=buttons_top_y - 12))

        # bouton Jouer
        play_button_y = buttons_top_y + 4
        self.btn_play.update()
        self.btn_play.draw(screen, self.font_label, self.font_sublabel, self.button_center_x, play_button_y, self.button_width)

        # bouton Règles (juste en dessous)
        rules_button_y = play_button_y + MenuButton.BUTTON_HEIGHT + 10
        self.btn_rules.update()
        self.btn_rules.draw(screen, self.font_label, self.font_sublabel, self.button_center_x, rules_button_y, self.button_width)

        # ---- Indicateur de version en bas de l'écran ----
        version_surf = self.font_version.render('v1.0  ·  USA MAP  ·  46 ÉTATS', True, C_TEXT_DIM)
        screen.blit(version_surf, version_surf.get_rect(centerx=center_x, y=self.screen_height - 28))

        # ---- Petites croix décoratives aux quatre coins ----
        corner_arm_size = 10
        corner_positions = [
            (40, 40),
            (self.screen_width - 40, 40),
            (40, self.screen_height - 40),
            (self.screen_width - 40, self.screen_height - 40)
        ]
        for corner_x, corner_y in corner_positions :
            pygame.draw.line(screen, C_BORDER, (corner_x - corner_arm_size, corner_y), (corner_x + corner_arm_size, corner_y), 1)
            pygame.draw.line(screen, C_BORDER, (corner_x, corner_y - corner_arm_size), (corner_x, corner_y + corner_arm_size), 1)

    def is_done(self) :
        """Retourne True quand le joueur a cliqué sur Jouer."""
        return self.result == 'play'
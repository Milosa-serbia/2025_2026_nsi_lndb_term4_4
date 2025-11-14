import pygame
from brbr_data import *
import math

class Button:
    def __init__(self, x, y, width, height, text, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.on_click = on_click

        self.base_color = pygame.Color(220, 220, 220)
        self.hover_color = pygame.Color(255, 255, 255)
        self.border_color = pygame.Color(50, 50, 50)
        self.text_color = pygame.Color(0, 0, 0)

        self.pressed = False

        # pré-rendu du texte
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def handle_event(self, event):
        # clic gauche
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.on_click is not None:
                    self.on_click()
            else:
                self.pressed = False

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # petite animation de "pulse" quand survolé
        t = pygame.time.get_ticks() / 200.0
        if hovered:
            pulse = 4 + 2 * math.sin(t)   # taille qui respire un peu
        else:
            pulse = 0

        draw_rect = self.rect.inflate(pulse, pulse)

        color = self.hover_color if hovered else self.base_color
        pygame.draw.rect(screen, color, draw_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, draw_rect, width=2, border_radius=10)

        # recentrer le texte dans le rect animé
        self.text_rect = self.text_surf.get_rect(center=draw_rect.center)
        screen.blit(self.text_surf, self.text_rect)



class UI :
    def __init__(self) :
        self.menu_open = False
        self.px_id = None
        self.back_menu_rect = pygame.rect.Rect(15, 15, 510, 820)
        self.menu_rect = pygame.rect.Rect(20, 20, 500, 810)
        self.font = pygame.font.Font(None, 32)
        self.title_font =pygame.font.Font(None, 50)

    
    def draw(self, screen, infos) :
        if self.menu_open :
            infos = infos[self.px_id]
            
            #  dessin du background du menu
            pygame.draw.rect(screen, (90, 90, 90), self.back_menu_rect)
            pygame.draw.rect(screen, (240, 240, 240), self.menu_rect)
            
            # textes du menu
            state_name = self.title_font.render('// ' + str(infos.name) + ' :', True, (0, 0, 0)) 
            alive_pop = self.font.render('- alive population : ' + str(int(infos.alive_population)), True, (0, 0, 0)) 
            # px_pop = self.font.render('- px population : ' + str(infos.population_per_px), True, (0, 0, 0)) 
            dead_pop = self.font.render('- dead/infected population : ' + str(int(infos.population - infos.alive_population)), True, (0, 0, 0)) 
            food_prod = self.font.render('- vegetable production : ' + str(int(infos.vegetable_production)), True, (0, 0, 0)) 
            food_ressources = self.font.render('- food ressources : ' + str(int(infos.food_ressources)), True, (0, 0, 0)) 
            importations = self.font.render('- importations :  ', True, (0, 0, 0)) 
            exportations = self.font.render('- exportations :  ', True, (0, 0, 0))
            border = self.font.render('- border statu :  ', True, (0, 0, 0))
            lockdown = self.font.render('- lockdown statu :  ', True, (0, 0, 0))
            
            # affichage des textes
            screen.blit(state_name, (70, 40))
            screen.blit(alive_pop, (40, 100))
            screen.blit(dead_pop, (40, 140))
            screen.blit(food_prod, (40, 180))
            screen.blit(food_ressources, (40, 220))
            screen.blit(importations, (40, 260))
            screen.blit(exportations, (40, 340))
            screen.blit(border, (40, 420))
            screen.blit(lockdown, (40, 460))
            
            
            
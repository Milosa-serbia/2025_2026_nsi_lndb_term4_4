import pygame
from brbr_data import *
import math

class Button:
    def __init__(self, x, y, width, height, font, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click

        self.base_color = pygame.Color(220, 220, 220)
        self.hover_color = pygame.Color(255, 255, 255)
        self.border_color = pygame.Color(50, 50, 50)
        self.text_color = pygame.Color(0, 0, 0)

        self.pressed = False


    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            if self.rect.collidepoint(event.pos) :
                if self.on_click is not None:
                    self.on_click()


    def draw(self, screen, text) :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # petite animation de "pulse" quand survolé
        t = pygame.time.get_ticks() / 200.0
        if hovered :
            pulse = 4 + 2 * math.sin(t)   # taille qui respire un peu
        else:
            pulse = 0

        draw_rect = self.rect.inflate(pulse, pulse)

        color = self.hover_color if hovered else self.base_color
        pygame.draw.rect(screen, color, draw_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, draw_rect, width=2, border_radius=10)

        # recentrer le texte dans le rect animé
        text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, self.text_rect)



class UI :
    def __init__(self, infos, closed_border_states, lockdowned_states) :
        self.px_id = None
        self.closed_border_states = closed_border_states
        self.lockdowned_states = lockdowned_states
        # attributs du menu
        self.menu_open = False
        self.back_menu_rect = pygame.rect.Rect(15, 15, 710, 820)
        self.menu_rect = pygame.rect.Rect(20, 20, 700, 810)
        self.decoration_rect1 = pygame.rect.Rect(35, 90, 660, 80)
        self.decoration_rect2 = pygame.rect.Rect(35, 190, 660, 120)
        self.decoration_rect3 = pygame.rect.Rect(35, 330, 660, 150)
        self.font = pygame.font.Font(None, 32)
        self.title_font =pygame.font.Font(None, 50)
        # attribus du menu 2
        self.menu2_open = False
        self.back_menu2_rect = pygame.rect.Rect(740, 15, 410, 520)
        self.menu2_rect = pygame.rect.Rect(745, 20, 400, 510)
        # boutons du menu
        self.exportation_button1 = Button(225, 395, 220, 35, self.font, self.open_menu2)
        self.exportation_button2 = Button(225, 435, 220, 35, self.font, self.open_menu2)
        self.exportation_button3 = Button(470, 395, 220, 35, self.font, self.open_menu2)
        self.exportation_button4 = Button(470, 435, 220, 35, self.font, self.open_menu2)
        self.border_button = Button(
            225, 495, 220, 35, self.font,
            lambda: self.change_border_statue(infos, self.closed_border_states)
        )
        self.lockdown_button = Button(
            260, 535, 220, 35, self.font,
            lambda: self.change_lockdown_statue(infos, self.lockdowned_states)
        )


    def change_border_statue(self, infos, closed_border_states) :
        if self.px_id in closed_border_states :
            closed_border_states.remove(self.px_id)
            infos[self.px_id].open_border = True
        else :
            closed_border_states.append(self.px_id)
            infos[self.px_id].open_border = False


    def change_lockdown_statue(self, infos, lockdowned_states) :
        if self.px_id in lockdowned_states :
            lockdowned_states.remove(self.px_id)
            infos[self.px_id].lockdown = False
        else :
            lockdowned_states.append(self.px_id)
            infos[self.px_id].lockdown = True


    def open_menu2(self) :
        if not self.menu2_open :
            self.menu2_open = True
        else :
            self.menu2_open = False


    def handle_input(self, events) :
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN :
                self.exportation_button1.handle_event(event)
                self.exportation_button2.handle_event(event)
                self.exportation_button3.handle_event(event)
                self.exportation_button4.handle_event(event)
                self.border_button.handle_event(event)
                self.lockdown_button.handle_event(event)
    
    
    def draw(self, screen, infos) :
        
        for id in self.closed_border_states :
            pygame.draw.rect(screen, (0, 255, 0), (infos[id].ui_pos[0], infos[id].ui_pos[1], 20, 20))
        
        if self.menu_open :
            id_infos = infos[self.px_id]
            
            #  dessin du background du menu
            pygame.draw.rect(screen, (90, 90, 90), self.back_menu_rect)
            pygame.draw.rect(screen, (235, 235, 235), self.menu_rect)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect1)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect2)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect3)
            
            # textes du menu
            state_name = self.title_font.render('// ' + str(id_infos.name) + ' :', True, (0, 0, 0)) 
            alive_pop = self.font.render('- Alive population : ' + str(int(id_infos.alive_population)), True, (0, 0, 0)) 
            # px_pop = self.font.render('- px population : ' + str(id_infos.population_per_px), True, (0, 0, 0)) 
            dead_pop = self.font.render('- Dead/infected population : ' + str(int(id_infos.population - id_infos.alive_population)), True, (0, 0, 0)) 
            obesity_rate = self.font.render('- Obesity rate : ' + str(id_infos.obesity_rate), True, (0, 0, 0)) 
            food_prod = self.font.render('- Vegetable production : ' + str(int(id_infos.vegetable_production)), True, (0, 0, 0)) 
            food_ressources = self.font.render('- Extra food ressources : ' + str(int(id_infos.food_ressources)), True, (0, 0, 0)) 
            importations = self.font.render('- Importations :  ', True, (0, 0, 0)) 
            exportations = self.font.render('- Exportations :  ', True, (0, 0, 0))
            border = self.font.render('- Open borders :  ', True, (0, 0, 0))
            lockdown = self.font.render('- Lockdown active :  ', True, (0, 0, 0))
            
            # affichage des textes
            screen.blit(state_name, (70, 40))
            screen.blit(alive_pop, (40, 100))
            screen.blit(dead_pop, (40, 140))
            screen.blit(obesity_rate, (40, 200))
            screen.blit(food_prod, (40, 240))
            screen.blit(food_ressources, (40, 280))
            screen.blit(importations, (40, 340))
            screen.blit(exportations, (40, 420))
            screen.blit(border, (40, 500))
            screen.blit(lockdown, (40, 540))
            
            # dessin des boutons
            export_texts = []
            for i in range(4) :
                try :
                    export_texts.append(infos[list(id_infos.exportations.keys())[i]].name)
                except :
                    export_texts.append('')
                    
            self.exportation_button1.draw(screen, export_texts[0])
            self.exportation_button2.draw(screen, export_texts[1])
            self.exportation_button3.draw(screen, export_texts[2])
            self.exportation_button4.draw(screen, export_texts[3])
            self.border_button.draw(screen, str(id_infos.open_border))
            self.lockdown_button.draw(screen, str(id_infos.lockdown))
            
            if self.menu2_open :
                #  dessin du background du menu 2
                pygame.draw.rect(screen, (90, 90, 90), self.back_menu2_rect)
                pygame.draw.rect(screen, (240, 240, 240), self.menu2_rect)
                
    
            
            
            
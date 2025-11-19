import pygame
from brbr_data import *
import math

class Button :
    def __init__(self, x, y, width, height, font, on_click=None) :
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


class Menu2Button:
    def __init__(self, x, y, width, height, font, text, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.on_click = on_click

        self.base_color = pygame.Color(220, 220, 220)   # couleur normale
        self.hover_color = pygame.Color(240, 240, 240)  # couleur au survol
        self.border_color = pygame.Color(50, 50, 50)    # bordure sombre
        self.text_color = pygame.Color(0, 0, 0)

    def handle_event(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()

    def draw(self, screen) :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # couleur selon survol
        color = self.hover_color if hovered else self.base_color

        # bouton carré
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, width=2)

        # texte centré
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    


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
        self.decoration_rect3 = pygame.rect.Rect(35, 330, 660, 85)
        self.decoration_rect4 = pygame.rect.Rect(35, 435, 660, 85)
        self.decoration_rect5 = pygame.rect.Rect(35, 540, 660, 165)
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 50)
        # attribus du menu 2
        self.menu2_open = False
        self.back_menu2_rect = pygame.rect.Rect(740, 15, 700, 820)
        self.menu2_rect = pygame.rect.Rect(745, 20, 690, 810)
        # boutons du menu
        self.exportation_index = None
        self.exportation_button1 = Button(225, 335, 220, 35, self.font, lambda: self.open_menu2(0))
        self.exportation_button2 = Button(225, 375, 220, 35, self.font, lambda: self.open_menu2(1))
        self.exportation_button3 = Button(470, 335, 220, 35, self.font, lambda: self.open_menu2(2))
        self.exportation_button4 = Button(470, 375, 220, 35, self.font, lambda: self.open_menu2(3))
        self.border_button = Button(
            420, 440, 220, 35, self.font,
            lambda: self.change_border_statue(infos, self.closed_border_states)
        )
        self.lockdown_button = Button(
            420, 480, 220, 35, self.font,
            lambda: self.change_lockdown_statue(infos, self.lockdowned_states)
        )
        # boutons du menu 2
        self.buttons_menu2 = []
        x1, y1 = 755, 30
        x2, y2 = 1005, 30
        x3, y3 = 1275, 30
        for id in range(101, 124):
            self.buttons_menu2.append(
                Menu2Button(
                    x1, y1, 225, 27, self.font, infos[id].name,
                    on_click=lambda id=id: self.change_exportation_id(infos, id)))
            y1 += 29

        for id in range(124, 147):
            self.buttons_menu2.append(
                Menu2Button(
                    x2, y2, 225, 27, self.font, infos[id].name,
                    on_click=lambda id=id: self.change_exportation_id(infos, id)))
            y2 += 29
            
        self.buttons_menu2.append(Menu2Button(
                    865, 710, 260, 40, self.font, 'None',
                    on_click=lambda: self.change_exportation_id(infos, 0)))

        for percent in range(0, 110, 10):
            self.buttons_menu2.append(
                Menu2Button(
                    x3, y3, 150, 35, self.font, f'{percent} %',
                    on_click=lambda p=percent: self.change_exportations_percent(infos, p)))
            y3 += 63
            
        # images
        self.lockdown_image = pygame.image.load("Enter.png").convert_alpha()
        self.lockdown_image = pygame.transform.scale(self.lockdown_image, (30, 30))
        self.closed_border_image = pygame.image.load("Locked.png").convert_alpha()
        self.closed_border_image = pygame.transform.scale(self.closed_border_image, (30, 30))
        self.closed_border_and_lockdown_image = pygame.image.load("Power.png").convert_alpha()
        self.closed_border_and_lockdown_image = pygame.transform.scale(self.closed_border_and_lockdown_image, (30, 30))
        

    def change_border_statue(self, infos, closed_border_states) :
        if self.px_id in closed_border_states :
            closed_border_states.remove(self.px_id)
            infos[self.px_id].closed_border = False
        else :
            if len(closed_border_states) < 4 :
                closed_border_states.append(self.px_id)
                infos[self.px_id].closed_border = True


    def change_lockdown_statue(self, infos, lockdowned_states) :
        if self.px_id in lockdowned_states :
            lockdowned_states.remove(self.px_id)
            infos[self.px_id].lockdown = False
        else :
            if len(lockdowned_states) < 4 :
                lockdowned_states.append(self.px_id)
                infos[self.px_id].lockdown = True


    def change_exportation_id(self, infos, new_export_id) :
        infos[self.px_id].exportations[self.exportation_index][0] = new_export_id
        infos[self.px_id].exportations[self.exportation_index][1] = 0
        if new_export_id != 0 :
            infos[new_export_id].importations.append(infos[self.px_id].name)
        # else :
            # infos[new_export_id].importations.remove(infos[self.px_id].name)


    def change_exportations_percent(self, infos, percent) :
        infos[self.px_id].exportations[self.exportation_index][1] = percent / 100


    def open_menu2(self, exportation_index) :
        self.exportation_index = exportation_index
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
                
                if self.menu2_open :
                    for button in self.buttons_menu2 :
                        button.handle_event(event)
    
    
    def draw(self, screen, infos) :
        
        closed_border_blits = self.closed_border_states.copy()
        for id in self.lockdowned_states :
            if id not in closed_border_blits :
                screen.blit(self.lockdown_image, (infos[id].ui_pos[0] - 5, infos[id].ui_pos[1] - 5))
            else :
                closed_border_blits.remove(id)
                screen.blit(self.closed_border_and_lockdown_image, (infos[id].ui_pos[0] - 5, infos[id].ui_pos[1] - 5))
        for id in closed_border_blits :
            screen.blit(self.closed_border_image, (infos[id].ui_pos[0] - 5, infos[id].ui_pos[1] - 5))
        
        if self.menu_open :
            id_infos = infos[self.px_id]
            
            #  dessin du background du menu
            pygame.draw.rect(screen, (90, 90, 90), self.back_menu_rect)
            pygame.draw.rect(screen, (235, 235, 235), self.menu_rect)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect1)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect2)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect3)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect4)
            pygame.draw.rect(screen, (250, 250, 250), self.decoration_rect5)
            
            # textes du menu
            state_name = self.title_font.render('// ' + str(id_infos.name) + ' :', True, (0, 0, 0)) 
            alive_pop = self.font.render('- Alive population : ' + str(int(id_infos.alive_population)), True, (0, 0, 0)) 
            dead_pop = self.font.render('- Dead/infected population : ' + str(int(id_infos.population - id_infos.alive_population)), True, (0, 0, 0)) 
            obesity_rate = self.font.render('- Obesity rate : ' + str(id_infos.obesity_rate), True, (0, 0, 0)) 
            food_prod = self.font.render('- Vegetable production : ' + str(int(id_infos.vegetable_production)), True, (0, 0, 0)) 
            food_ressources = self.font.render('- Food ressources : ' + str(int(id_infos.food_ressources)), True, (0, 0, 0)) 
            importations = self.font.render('- Importations : ', True, (0, 0, 0)) 
            exportations = self.font.render('- Exportations : ', True, (0, 0, 0))
            border = self.font.render('- Closed borders (max : 4 states) :  ', True, (0, 0, 0))
            lockdown = self.font.render('- Lockdown active (max : 4 states) :  ', True, (0, 0, 0))
            
            # affichage des textes
            screen.blit(state_name, (70, 40))
            screen.blit(alive_pop, (40, 100))
            screen.blit(dead_pop, (40, 140))
            screen.blit(obesity_rate, (40, 200))
            screen.blit(food_prod, (40, 240))
            screen.blit(food_ressources, (40, 280))
            screen.blit(exportations, (40, 360))
            screen.blit(border, (40, 445))
            screen.blit(lockdown, (40, 485))
            screen.blit(importations, (40, 550))
            
            x, y = 230, 550
            for export in id_infos.importations : 
                text = self.font.render(f'{export}', True, (0, 0, 0))
                screen.blit(text, (x, y))
                y += 40
                
            # dessin des boutons
            export_texts = []
            for i in range(4) :
                try :
                    export_texts.append(infos[id_infos.exportations[i][0]].name)
                except :
                    export_texts.append('')
                    
            self.exportation_button1.draw(screen, export_texts[0])
            self.exportation_button2.draw(screen, export_texts[1])
            self.exportation_button3.draw(screen, export_texts[2])
            self.exportation_button4.draw(screen, export_texts[3])
            self.border_button.draw(screen, str(id_infos.closed_border))
            self.lockdown_button.draw(screen, str(id_infos.lockdown))
            
            if self.menu2_open :
                #  dessin du background du menu 2
                pygame.draw.rect(screen, (90, 90, 90), self.back_menu2_rect)
                pygame.draw.rect(screen, (240, 240, 240), self.menu2_rect)
                for button in self.buttons_menu2 :
                    button.draw(screen)
                    
                if id_infos.exportations[self.exportation_index][0] != 0 :
                    percent_text = self.font.render('Actual : ' + str(int(id_infos.exportations[self.exportation_index][1] * 100)) + '%', True, (0, 0, 0)) 
                    name_export_text = self.font.render('Actual : ' + infos[id_infos.exportations[self.exportation_index][0]].name, True, (0, 0, 0)) 
                    screen.blit(percent_text, (1280, 765))
                    screen.blit(name_export_text, (865, 765))
    
            
            
            
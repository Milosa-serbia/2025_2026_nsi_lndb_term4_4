import pygame
from brbr_data import *

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
            pygame.draw.rect(screen, (90, 90, 90), self.back_menu_rect)
            pygame.draw.rect(screen, (240, 240, 240), self.menu_rect)
            state_name = self.title_font.render('// ' + str(infos.name) + ' :', True, (0, 0, 0)) 
            alive_pop = self.font.render('- alive population : ' + str(int(infos.alive_population)), True, (0, 0, 0)) 
            px_pop = self.font.render('- px population : ' + str(infos.population_per_px), True, (0, 0, 0)) 
            dead_pop = self.font.render('- dead/infected population : ' + str(int(infos.population - infos.alive_population)), True, (0, 0, 0)) 
            screen.blit(state_name, (70, 40))
            screen.blit(alive_pop, (40, 100))
            screen.blit(px_pop, (40, 140))
            screen.blit(dead_pop, (40, 180))
            
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
            screen.blit(state_name, (70, 40))
            screen.blit(alive_pop, (40, 100))
            
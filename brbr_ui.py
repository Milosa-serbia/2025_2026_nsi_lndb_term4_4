import pygame
from brbr_data import *

class UI :
    def __init__(self) :
        self.menu_open = False
        self.px_id = None
        self.menu_rect = pygame.rect.Rect(20, 20, 500, 810)
        self.font = pygame.font.Font(None, 32)

    
    def draw(self, screen, infos) :
        if self.menu_open :
            infos = infos[self.px_id]
            pygame.draw.rect(screen, (240, 240, 240), self.menu_rect)
            state_name = self.font.render(str(infos.name), True, (0, 0, 0)) 
            screen.blit(state_name, (40, 40))
            
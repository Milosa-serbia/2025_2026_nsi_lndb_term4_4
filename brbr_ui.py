import pygame

class UI :
    def __init__(self) :
        self.menu_open = False
        self.px_id = None
        self.status_rect = pygame.rect.Rect(20, 20, 500, 810)
        self.infos = None
    
    def draw(self, screen) :
        if self.menu_open :
            pygame.draw.rect(screen, (240, 240, 240), self.status_rect)
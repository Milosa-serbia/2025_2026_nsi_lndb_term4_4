import pygame

class Map :
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        self.width, self.height = self.screen.get_size()
        self.cell_size = 4
        
        self.first_px_pos = 100, 100
        
        self.px_infected = []
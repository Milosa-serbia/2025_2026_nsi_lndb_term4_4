import pygame

class Map :
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        self.width, self.height = self.screen.get_size()
        self.cell_size = 4
        
        self.first_px_pos = 100, 100
        
        self.pixels_infected_pos = []
        
    def update_infection(self) : 
        for px_infected in self.pixels_infected_pos :
            self.pixels_infected_pos.append((px_infected[0], px_infected[1] + 1))
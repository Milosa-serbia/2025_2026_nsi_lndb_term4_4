import pygame, sys
from map import *

class Simulation:
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        self.clock = pygame.time.Clock()
        
        self.map = Map()


    def draw_map(self) : 
        cell_size = self.map.cell_size
        
        for x in range(0,  self.map.width, cell_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.map.height))
        for y in range(0, self.map.height, cell_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.map.width, y))
            
        first_px_x = self.map.first_px_pos[0]
        first_px_y = self.map.first_px_pos[1]
        
        self.map.pixels_infected_pos.append((first_px_x, first_px_y))
        for px_pos in self.map.pixels_infected_pos :
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(px_pos[0], px_pos[1], cell_size, cell_size))
        
        
    def run(self) :
        while True:
            self.clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.draw_map()
            self.map.update_infection()
            pygame.display.update()


simulation = Simulation()
simulation.run()

            
        
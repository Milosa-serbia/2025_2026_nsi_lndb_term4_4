import pygame, sys
import pytmx
from map import *

class Simulation:
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        self.clock = pygame.time.Clock()
        
        self.infection = Infection()
        # self.map_image = pygame.image.load('carte_us_pixel.png')
        # self.map_image = pygame.transform.scale_by(self.map_image, 2).convert_alpha()
        
        # self.tmx = pytmx.util_pygame.load_pygame('carte_usa.tmx')

    def draw_map(self) : 
        cell_size = self.infection.cell_size
            
        for pos in self.infection.infected_pixels_pos :
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(pos[0], pos[1], cell_size, cell_size))
        # for p in self.infection.dead_pixels_pos :
        #     pygame.draw.rect(self.screen, (128, 128, 128), pygame.Rect(p[0], p[1], cell_size, cell_size))
        
        
    def run(self) :
        while True:
            self.clock.tick(360)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("white")
            self.draw_map()
            # self.debug_layer('frontieres')
            # self.draw_tile_top_left_pixels('frontieres')
            self.infection.update_infection()
            pygame.display.update()


simulation = Simulation()
simulation.run()

            
        
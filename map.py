import pygame
import random

class Map :
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        self.width, self.height = self.screen.get_size()
        self.cell_size = 1
        self.time_last_simulation = 0
        
        self.infected_pixels_pos = {(100, 100), (700, 400), (500, 500)}
        self.dead_pixels_pos = set()

    def update_infection(self) :
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_simulation >= 1000 :
            self.time_last_simulation = pygame.time.get_ticks()
            
            new_infected = set()
            for x, y in self.infected_pixels_pos :
                if (x, y) not in self.dead_pixels_pos :
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1, 1), (-1, -1), (1, -1), (-1, 1)] :
                        if (x + dx <= 1600) and (y + dy <= 900) and ((x+dx, y+dy) not in self.infected_pixels_pos) :
                            random_number = random.randint(1, 15)
                            if random_number in [1, 2] :
                                new_infected.add((x+dx, y+dy))
            self.infected_pixels_pos |= new_infected  # union des sets
            
            for pixels in self.infected_pixels_pos :
                random_number_2 = random.randint(1, 30)
                if random_number_2 in [1] :
                    self.dead_pixels_pos.add(pixels)
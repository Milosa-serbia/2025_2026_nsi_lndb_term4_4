import pygame
import random

class Infection :
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        self.width, self.height = self.screen.get_size()
        self.cell_size = 1
        self.time_last_infection = 0
        self.air_transmission_is_active = True
        
        self.infected_pixels_pos = {(700, 400)}
        self.dead_pixels_pos = set()


    def contact_transmission(self) : # ça marche pas trop 
        new_infected = set()
        for x, y in self.infected_pixels_pos :
            if (x, y) not in [self.dead_pixels_pos, self.infected_pixels_pos] :
                for dx, dy in [(self.cell_size, 0), (-self.cell_size, 0), (0,self.cell_size) , (0,-self.cell_size) , (self.cell_size,  self.cell_size) , (-self.cell_size,  -self.cell_size) , (self.cell_size,  -self.cell_size) , (-self.cell_size,  self.cell_size) ] :
                    if (0-dx <= x + dx <= 1400) and \
                        (0-dx <= y + dy <= 800) and \
                        ((x+dx, y+dy) not in self.infected_pixels_pos) and \
                        ((x+dx, y+dy) not in self.dead_pixels_pos) :
                            if random.randint(1, 15) in [1, 2] :
                                new_infected.add((x+dx, y+dy))       
        self.infected_pixels_pos |= new_infected  # union des sets


    def air_transmission(self) :
        if self.air_transmission_is_active and random.randint(1, 100) == 1 :
            new_pixel_infected_x = 700
            new_pixel_infected_y = 400
            while (new_pixel_infected_x, new_pixel_infected_y) in self.infected_pixels_pos or \
            (new_pixel_infected_x, new_pixel_infected_y) in self.dead_pixels_pos : # pk la 2eme verif?
                reference_pixel = list(self.infected_pixels_pos)[random.randint(0, len(self.infected_pixels_pos) - 1)]
                new_pixel_infected_x = reference_pixel[0] + random.randint(-400, 400)
                new_pixel_infected_y = reference_pixel[1] + random.randint(-400, 400)
            
            self.infected_pixels_pos.add((new_pixel_infected_x, new_pixel_infected_y))
            

    def update_infected_number(self) :
        self.contact_transmission()
        self.air_transmission()

    def update_dead_number(self) :
        infected_pixels = self.infected_pixels_pos.copy()
        for pixel in infected_pixels :
                if random.randint(1, 15) == 1 :
                    self.dead_pixels_pos.add(pixel)
                    self.infected_pixels_pos.remove(pixel)


    def update_infection(self) :
        current_time = pygame.time.get_ticks()
        if current_time - self.time_last_infection >= 10 :
            self.time_last_infection = pygame.time.get_ticks()
            
            self.update_infected_number()
            self.update_dead_number()
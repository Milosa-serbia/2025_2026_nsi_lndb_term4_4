import pygame, sys
from brbr_infection import *
from brbr_ui import *
from brbr_continent import *

class Simulation :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 850))
        pygame.display.set_caption("Infection NumPy")
        self.clock = pygame.time.Clock()
        self.continent = Continent()

    def run(self) :
        while True :
            self.clock.tick(60)
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

            # Draw
            self.continent.update_and_draw(events)
            pygame.display.update()

if __name__ == "__main__" :
    sim = Simulation()
    sim.run()

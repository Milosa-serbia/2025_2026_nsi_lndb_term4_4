
import pygame, sys
from map import Infection

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Infection NumPy — 0 = safe, 1 = infected")
        self.clock = pygame.time.Clock()
        self.infection = Infection()

    def run(self):
        while True:
            self.clock.tick(360)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.infection.update_infection()

            # Draw
            self.infection.draw(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()

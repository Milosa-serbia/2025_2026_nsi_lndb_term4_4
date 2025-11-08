import pygame, sys
from map import Infection

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 850))
        pygame.display.set_caption("Infection NumPy")
        self.clock = pygame.time.Clock()
        self.infection = Infection()
        self.pause = False

    def run(self):
        while True :
            self.clock.tick(360)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE :
                        if self.pause == False :
                            self.pause = True
                        else : 
                            self.pause = False

            if self.pause == False :
                self.infection.update_infection()

            # Draw
            self.infection.draw(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()

import pygame, sys
from brbr_infection import *
from brbr_ui import *

class Simulation :
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 850))
        pygame.display.set_caption("Infection NumPy")
        self.clock = pygame.time.Clock()
        self.infection = Infection()
        self.ui = UI()

    def run(self) :
        while True :
            self.clock.tick(60)
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
                            
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if not self.ui.menu_open :
                        self.ui.px_id = self.infection.state_grid[int(y), int(x)]
                        if self.ui.px_id not in self.infection.invalid_statues_for_contamination :   
                            self.ui.menu_open = True
                    else :
                        if not self.ui.status_rect.collidepoint(x, y) :
                            self.ui.menu_open = False
                        
            # Update
            self.infection.update_infection()

            # Draw
            self.infection.draw(self.screen, self.ui.menu_open)
            self.ui.draw(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()

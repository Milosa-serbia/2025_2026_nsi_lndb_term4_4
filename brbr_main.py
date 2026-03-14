import pygame, sys
from brbr_menu import MainMenu
from brbr_continent import Continent


class Simulation :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 850))
        pygame.display.set_caption("Pathogen")
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(1500, 850)
        self.continent = None  # créé seulement après validation du menu

    def run(self) :
        while True :
            self.clock.tick(60)
            events = pygame.event.get()

            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

            # ---- Phase menu ----
            if self.continent is None :
                for event in events :
                    self.menu.handle_event(event)
                self.menu.update()
                self.menu.draw(self.screen)

                # le joueur a cliqué sur "Jouer"  : on lance la simulation
                if self.menu.is_done() :
                    self.continent = Continent()

            # ---- Phase jeu ----
            else :
                self.continent.update_and_draw(events)

            pygame.display.update()


if __name__ == "__main__" :
    sim = Simulation()
    sim.run()

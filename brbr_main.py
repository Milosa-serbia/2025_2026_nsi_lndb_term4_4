import pygame, sys
import pytmx
from map import *

class Simulation:
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        self.clock = pygame.time.Clock()
        
        self.infection = Infection()
        self.map_image = pygame.image.load('carte_us_pixel.png')
        self.map_image = pygame.transform.scale_by(self.map_image, 2).convert_alpha()  # x4
        
        self.tmx = pytmx.util_pygame.load_pygame('carte_usa.tmx')

    def draw_map(self) : 
        cell_size = self.infection.cell_size
            
        for pos in self.infection.infected_pixels_pos :
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(pos[0], pos[1], cell_size, cell_size))
        for p in self.infection.dead_pixels_pos :
            pygame.draw.rect(self.screen, (128, 128, 128), pygame.Rect(p[0], p[1], cell_size, cell_size))


    # def debug_layer(self, layer_name):
    #     layer = self.tmx.get_layer_by_name(layer_name)
    #     total = 0
    #     non_empty = 0
    #     gids = {}
    #     for x, y, gid in layer:
    #         total += 1
    #         if gid:
    #             non_empty += 1
    #             gids[gid] = gids.get(gid, 0) + 1
    #     print(f"[{layer_name}] cases totales: {total}, tuiles posées: {non_empty}")
    #     # Top 10 GIDs les plus fréquents
    #     top = sorted(gids.items(), key=lambda kv: kv[1], reverse=True)[:10]
    #     print("Top GIDs:", top)


    # def draw_tile_top_left_pixels(self, layer_name):
    #     tw, th = self.tmx.tilewidth, self.tmx.tileheight
    #     layer = self.tmx.get_layer_by_name(layer_name)

    #     # IMPORTANT : on saute les cases vides (gid == 0)
    #     for x, y, gid in layer:
    #         if gid == 0:
    #             continue
    #         px = x * tw
    #         py = y * th
    #         pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(px, py, 1, 1))

        
        
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

            
        
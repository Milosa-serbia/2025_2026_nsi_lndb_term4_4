import numpy as np
import pygame

WIDTH = 1400
HEIGHT = 800


def grid_to_surf(gray_2d: np.ndarray, surf:pygame.Surface) -> pygame.Surface :
    # Étend (H,W) -> (H,W,1) -> (H,W,3)
    rgb = np.repeat(gray_2d[:, :, None], 3, axis=2)      # (H, W, 3)
    rgb = np.transpose(rgb, (1, 0, 2))                   # (W, H, 3) pour Pygame
    pygame.surfarray.blit_array(surf, rgb)
    return surf


def main() :
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid  = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    print(grid)
    clock = pygame.time.Clock()
    surf = pygame.Surface((WIDTH, HEIGHT))
    drawing = False
    
    running = True
    while running :
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 : 
                drawing = False
        
        if drawing : 
            x, y = pygame.mouse.get_pos()
            if 0 - 1<= x <= WIDTH - 1 and 0 - 1<= y <= HEIGHT - 1 :
                grid[y, x] = 255

        surf = grid_to_surf(grid, surf)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(1000)  
                
main()
import numpy as np
import pygame

WIDTH = 1400
HEIGHT = 800


def grid_to_surf(gray_2d, surf):
    # Étend (H,W) -> (H,W,1) -> (H,W,3)
    rgb = np.repeat(gray_2d[:, :, None], 3, axis=2)      # (H, W, 3)
    rgb = np.transpose(rgb, (1, 0, 2))                   # (W, H, 3) pour Pygame
    pygame.surfarray.blit_array(surf, rgb)
    return surf


def save_grid(grid, filename="dessin.npy"):
    np.save(filename, grid)
    print(f"Tableau NumPy sauvegardé sous {filename}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    try :
        grid  = np.load('dessin.npy')
    except :
        grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    
    clock = pygame.time.Clock()
    surf = pygame.Surface((WIDTH, HEIGHT))
    drawing = False
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
                drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:   # touche "s" pour sauvegarder
                    save_grid(grid)
                    
                if event.key == pygame.K_z :
                    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

        if drawing: 
            x, y = pygame.mouse.get_pos()
            if 0 <= x < WIDTH - 2 and 0 <= y < HEIGHT - 2:
                grid[y:y+5, x:x+5] = 255  # petit carré de 3x3

        surf = grid_to_surf(grid, surf)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(1000)  
    
    pygame.quit()
                
main()

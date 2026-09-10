import pygame
import sys
from constants import *

def main():
    # This is the intialization phase
    pygame.init() # The whole reason this works
    clock = pygame.time.Clock() # Calculating FPS using the computers clock
    dt:float = 0.0 # Delta Time
    
    # This is for the display to view the game through
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense")

    # This will be the game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((1, 2, 3))

        # Rerenders above to screen at 60 FPS (Adjustable FPS)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()



if __name__ == "__main__":
    main()

import pygame
import sys
from constants import *

def main():
    pygame.init() # The whole reason this works
    
    # This is for the display to view the game through
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # This will be the game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((1, 2, 3))

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

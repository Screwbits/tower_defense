import pygame
import sys
from enemy import Enemy
from constants import *

def main():
    # This is the intialization phase
    pygame.init() # The whole reason this works
    clock = pygame.time.Clock() # Calculating FPS using the computers clock
    dt:float = 0.0 # Delta Time
    
    # This is for the display to view the game through
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense")

    # This is responsible for dealing with textures and images
    enemy_image = pygame.image.load('assets/images/enemies/enemy1.png').convert_alpha()

    # This will hold the groups that contain all the sprites (objects)
    enemy_group = pygame.sprite.Group()

    enemy = Enemy((500, 500), enemy_image)
    enemy_group.add(enemy)
    print(enemy) # Shows if enemy has been spawn or not for console debugging

    # This will be the game Loop
    while True:
        clock.tick(FPS)

        # Background rendered first
        screen.fill((1, 100, 3))

        # Update groups
        enemy_group.update()

        # Draws groups
        enemy_group.draw(screen)

        # Accounts for events that happen in game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        

        # Rerenders above to screen at 60 FPS (Adjustable FPS)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

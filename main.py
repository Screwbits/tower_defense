import pygame
import sys
import json
from enemy import Enemy
from constants import *
from world import World
from turret import Turret
from button import Button


def main():
    # This is the intialization phase
    pygame.init() # The whole reason this works
    clock = pygame.time.Clock() # Calculating FPS using the computers clock
    
    # This is for the display to view the game through
    screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_PANEL, SCREEN_HIGHT))
    pygame.display.set_caption("Tower Defense")

    # Game Variables
    placing_turrets = False

    # This is responsible for dealing with textures and images
    map_image = pygame.image.load('levels/level1.png').convert_alpha()
    # individual turrets image for mouse cursor
    currsor_turret = pygame.image.load('assets/images/turrets/currsor_turret.png').convert_alpha()
    # enemys
    enemy_image = pygame.image.load('assets/images/enemies/enemy1.png').convert_alpha()
    # The buttons to work the turrets
    buy_turret_image = pygame.image.load('assets/images/buttons/buy_button.png').convert_alpha()
    cancel_image = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
    

    # Load json data into level
    with open('levels/level1.tmj') as file:
        world_data = json.load(file)

    def create_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE
        # Calculate sequential number of tiles
        mouse_tile_num = (mouse_tile_y * COLS) + mouse_tile_x
        # check if tile is grass
        if world.tile_map[mouse_tile_num] != 5:
            # Check for redunant turrets at tile
            space_is_free = True
            for turret in turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
            if space_is_free == True:
                new_turret = Turret(currsor_turret, mouse_tile_x, mouse_tile_y)
                turret_group.add(new_turret)


    # Create World
    world = World(world_data, map_image)
    world.process_data()


    # This will hold the groups that contain all the sprites (objects)
    enemy_group = pygame.sprite.Group()
    turret_group = pygame.sprite.Group()
    enemy = Enemy(world.waypoints, enemy_image)
    enemy_group.add(enemy)

    # Create the Buttons
    turret_button = Button(SCREEN_WIDTH + 30, 120, buy_turret_image, True)
    cancel_button = Button(SCREEN_WIDTH + 50, 180, cancel_image, True)


    # This will be the game Loop
    while True:
        clock.tick(FPS)

        #################################
        # UPDATING SECTION
        #################################

         # Update groups
        enemy_group.update()

        #################################
        # DRAWING SECTION
        #################################

        screen.fill((1, 0, 200))

        # Background rendered first
        world.draw(screen) # put after screen.fill()

        # Draws groups
        enemy_group.draw(screen)
        turret_group.draw(screen)

        # Draw buttons
        if turret_button.draw(screen): # Button to buy the turrets
            placing_turrets = True
        
        # Shows cancel button only if buy turret has been clicked
        if placing_turrets == True:
            # Show currsor turret
            currsor_rect = currsor_turret.get_rect()
            currsor_pos = pygame.mouse.get_pos()
            currsor_rect.center = currsor_pos
            if currsor_pos[0] <= SCREEN_WIDTH:
                screen.blit(currsor_turret, currsor_rect)
            if cancel_button.draw(screen): # Button to stop buying
                placing_turrets = False

        # Accounts for events that happen in game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # mouse click (event.button == 1 means on left click)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # check if mouse is in the game area
                if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[0] < SCREEN_HIGHT:
                    if placing_turrets == True:
                        create_turret(mouse_pos)
        

        # Rerenders above to screen at 60 FPS (Adjustable FPS)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

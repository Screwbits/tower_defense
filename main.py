import pygame
import sys
import json
from enemy import Enemy
from constants import *
from world import World
from turret import Turret

# NOTE: fix the path finding in the world.py file (or just redo the assets)



def main():
    # This is the intialization phase
    pygame.init() # The whole reason this works
    clock = pygame.time.Clock() # Calculating FPS using the computers clock
    
    # This is for the display to view the game through
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
    pygame.display.set_caption("Tower Defense")

    # This is responsible for dealing with textures and images
    map_image = pygame.image.load('levels/level.png').convert_alpha()
    currsor_turret = pygame.image.load('assets/images/turrets/currsor_turret.png').convert_alpha()
    enemy_image = pygame.image.load('assets/images/enemies/enemy1.png').convert_alpha()
    

    # Load json data into level
    with open('levels/level.tmj') as file:
        world_data = json.load(file)

    def create_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE
        # Calculate sequential number of tiles
        mouse_tile_num = (mouse_tile_y * COLS) + mouse_tile_x
        # check if tile is grass
        if world.tile_map[mouse_tile_num] != 8:
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
    print(world.waypoints)

    # This will be the game Loop
    while True:
        clock.tick(FPS)

        # Background rendered first
        screen.fill((1, 100, 3))
        world.draw(screen) # put after screen.fill()
        pygame.draw.lines(screen, "grey0", False, world.waypoints)

        # Update groups
        enemy_group.update()

        # Draws groups
        enemy_group.draw(screen)
        turret_group.draw(screen)

        # Accounts for events that happen in game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # mouse click (event.button == 1 means on left click)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # check if mouse is in the game area
                if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[0] < SCREEN_HIGHT:
                    create_turret(mouse_pos)
        

        # Rerenders above to screen at 60 FPS (Adjustable FPS)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

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
    last_enemy_spawn = pygame.time.get_ticks()
    placing_turrets = False
    selected_turret = None

    # This is responsible for dealing with textures and images
    map_image = pygame.image.load('levels/level1.png').convert_alpha()
    # Turret Sprite Sheets
    turret_spritesheets = []

    for x in range(1, TURRET_LEVELS + 1):
        turret_sheet = pygame.image.load(f'assets/images/turrets/turret{x}.png').convert_alpha()
        turret_spritesheets.append(turret_sheet)
    
    # individual turrets image for mouse cursor
    currsor_turret = pygame.image.load('assets/images/turrets/currsor_turret.png').convert_alpha()
    # enemies
    enemy_images = {
        "weak": pygame.image.load('assets/images/enemies/enemy1.png').convert_alpha(),
        "medium": pygame.image.load('assets/images/enemies/enemy2.png').convert_alpha(),
        "strong": pygame.image.load('assets/images/enemies/enemy3.png').convert_alpha(),
        "elite": pygame.image.load('assets/images/enemies/enemy4.png').convert_alpha()
    }
    enemy_image = pygame.image.load('assets/images/enemies/enemy1.png').convert_alpha()
    # The buttons to work the turrets
    buy_turret_image = pygame.image.load('assets/images/buttons/buy_button.png').convert_alpha()
    cancel_image = pygame.image.load('assets/images/buttons/cancel_button.png').convert_alpha()
    upgrade_turret_image = pygame.image.load('assets/images/buttons/upgrade_turret_button.png').convert_alpha()
    

    # Load json data into level
    with open('levels/level1.tmj') as file:
        world_data = json.load(file)

    # Load fonts for displaying text on screen
    text_font = pygame.font.SysFont("Consolas", 24, bold = True)
    large_font = pygame.font.SysFont("Consolas", 36)

    # Function for outputting text onto window screen
    def draw_text(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))

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
                new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
                turret_group.add(new_turret)
                # Deduct cost of turret
                world.money -= BUY_COST

    def select_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // TILE_SIZE
        mouse_tile_y = mouse_pos[1] // TILE_SIZE
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret

    def clear_selection():
        for turret in turret_group:
            turret.selected = False

    # Create World
    world = World(world_data, map_image)
    world.process_data()
    world.process_enemies()


    # This will hold the groups that contain all the sprites (objects)
    enemy_group = pygame.sprite.Group()
    turret_group = pygame.sprite.Group()


    # Create the Buttons
    turret_button = Button(SCREEN_WIDTH + 30, 120, buy_turret_image, True)
    cancel_button = Button(SCREEN_WIDTH + 50, 180, cancel_image, True)
    upgrade_button = Button(SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)


    # This will be the game Loop
    while True:
        clock.tick(FPS)

        #################################
        # UPDATING SECTION
        #################################

        # Update groups
        enemy_group.update(world)
        turret_group.update(enemy_group)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

        #################################
        # DRAWING SECTION
        #################################

        screen.fill((1, 0, 200))

        # Background rendered first
        world.draw(screen) # put after screen.fill()

        # Draws groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        draw_text(str(world.health), text_font, "grey100", 0, 0)
        draw_text(str(world.money), text_font, "grey100", 0, 30)

        # Spawn Enemies
        if pygame.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
            if world.spawned_enemies < len(world.enemy_list):
                enemy_type = world.enemy_list[world.spawned_enemies]
                enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                enemy_group.add(enemy)
                world.spawned_enemies += 1
                last_enemy_spawn = pygame.time.get_ticks()

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

        # Show upgrade button if selected
        if selected_turret:
            if selected_turret.upgrade_level < TURRET_LEVELS:
                if upgrade_button.draw(screen):
                    if world.money >= UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= UPGRADE_COST

        # Accounts for events that happen in game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # mouse click (event.button == 1 means on left click)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # check if mouse is in the game area
                if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[0] < SCREEN_HIGHT:
                    # Clear selected turrets
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        # Check if you have the money to place turrets
                        if world.money >= BUY_COST:
                            create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)
        

        # Rerenders above to screen at 60 FPS (Adjustable FPS)
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

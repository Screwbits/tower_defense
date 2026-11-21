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
    game_over = False
    game_outcome = 0 # -1 is a loss, 1 is a win
    level_started = False
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
    begin_image = pygame.image.load('assets/images/buttons/new_wave_button.png').convert_alpha()
    restart_image = pygame.image.load('assets/images/buttons/restart_button.png').convert_alpha()
    fast_forward_image = pygame.image.load('assets/images/buttons/fast_forward_button.png').convert_alpha()
    # GUI
    heart_image = pygame.image.load('assets/images/gui/heart.png').convert_alpha()
    money_image = pygame.image.load('assets/images/gui/money.png').convert_alpha()
    logo_image = pygame.image.load('assets/images/gui/logo.png').convert_alpha()
    
    # load sound
    shot_fx = pygame.mixer.Sound('assets/audio/royalty_free_canon.wav')
    shot_fx.set_volume(0.5)

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

    # Holds all the data to build a display panel
    def display_panel():
        # Main body of panel
        pygame.draw.rect(screen, "aquamarine", (SCREEN_WIDTH, 0, SIDE_PANEL, SCREEN_HIGHT))
        pygame.draw.rect(screen, "grey0", (SCREEN_WIDTH, 0, SIDE_PANEL, 400), 5)
        screen.blit(logo_image, (SCREEN_WIDTH, 400))
        # Information the panel holds
        draw_text("WAVE: " + str(world.level), text_font, "grey10", SCREEN_WIDTH + 10, 10)
        screen.blit(heart_image, (SCREEN_WIDTH + 10, 35))
        draw_text(str(world.health), text_font, "grey10", SCREEN_WIDTH + 50, 40)
        screen.blit(money_image, (SCREEN_WIDTH + 10, 65))
        draw_text(str(world.money), text_font, "grey10", SCREEN_WIDTH + 50, 70)

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
                new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
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
    begin_button = Button(SCREEN_WIDTH + 60, 300, begin_image, True)
    restart_button = Button(310, 300, restart_image, True)
    fast_forward_button = Button(SCREEN_WIDTH + 55, 300, fast_forward_image, False)


    # This will be the game Loop
    while True:
        clock.tick(FPS)

        #################################
        # UPDATING SECTION
        #################################

        if game_over == False:
            # Check if player has lost
            if world.health <= 0:
                game_over = True
                game_outcome = -1 # You Lost
            # Check if player has won
            if world.level > TOTAL_LEVELS:
                game_over = True
                game_outcome = 1 # You Won

            # Update groups
            enemy_group.update(world)
            turret_group.update(enemy_group, world)

            # Highlight selected turret
            if selected_turret:
                selected_turret.selected = True

        #################################
        # DRAWING SECTION
        #################################

        # Background rendered first
        world.draw(screen) # put after screen.fill()

        # Draws groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

        # Has all the data to build a display panel
        display_panel()

        if game_over == False:
            # Check if the level has been started or not
            if level_started == False:
                if begin_button.draw(screen):
                    level_started = True
            else:
                # fast forward option here
                world.game_speed = 1
                if fast_forward_button.draw(screen):
                    world.game_speed = 2
                # Spawn Enemies
                if pygame.time.get_ticks() - last_enemy_spawn > SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pygame.time.get_ticks()

            # Check if the wave is finished
            if world.check_level_complete() == True:
                world.money += LEVEL_COMPLETE_REWARD
                world.level += 1
                level_started = False
                last_enemy_spawn = pygame.time.get_ticks()
                world.reset_level()
                world.process_enemies()

            # Draw buttons
            #--------------------------------------------------
            # Print out text for how much the turret costs
            screen.blit(money_image, (SCREEN_WIDTH + 140, 120))
            draw_text(str(BUY_COST), text_font, "grey10", SCREEN_WIDTH + 95, 125)
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
                    # Show the cost for the upgrade
                    screen.blit(money_image, (SCREEN_WIDTH + 160, 180))
                    draw_text(str(UPGRADE_COST), text_font, "grey10", SCREEN_WIDTH + 115, 185)
                    if upgrade_button.draw(screen):
                        if world.money >= UPGRADE_COST:
                            selected_turret.upgrade()
                            world.money -= UPGRADE_COST
        else:
            pygame.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
            if game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("YOU WON!", large_font, "grey0", 315, 230)

            if restart_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                # Empty the Groups
                enemy_group.empty()
                turret_group.empty()

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

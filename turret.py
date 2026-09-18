import pygame
import constants as c

class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pygame.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 1500
        self.last_shot = pygame.time.get_ticks()
        self.selected = False

        # Position Variables
        self.tile_x = tile_x
        self.tile_y = tile_y

		# Calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        
        # Animation Variables
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        # update image section
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self):
        # Extract images from sprite sheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self):
        # Search for new target once turret has cooled down
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()

        

    def play_animation(self):
        # update image
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed to since last update
        if pygame.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            # Check if animation is done and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Records completed time so turret can start cooling down
                self.last_shot = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected == True:
            surface.blit(self.range_image, self.range_rect)
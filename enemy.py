import pygame
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA

# inherets functionality from pygame.sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(waypoints[0])
        self.target_waypoint = 1
        self.heath = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Define a target waypoint
        if self.target_waypoint < len(self.waypoints):
        	self.target = Vector2(self.waypoints[self.target_waypoint])
        	self.movement = self.target - self.pos
        else:
        	# Enemy has reached end of the path
            self.kill()

		# Calculate distance to target
        dist = self.movement.length()
		# Check if remaining distance is greater than enemey speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed # Does the trianometry work
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.pos

    def rotate(self):
		# calculate distance to next waypoint
        dist = self.target - self.pos
		# use distance to calculate
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
		# rotate image and update rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
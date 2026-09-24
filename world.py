import pygame
import constants as c
import random
import enemy_data from ENEMY_SPAWN_DATA

class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0

    def process_data(self):
		# Look through data to extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap_1":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)
	
    def process_waypoints(self, data):
		# Iterate through data to extract x and y coordinates
        for point in data:
            temp_x = point.get("x") + c.TILE_SIZE * c.COLS
            temp_y = point.get("y") + (c.TILE_SIZE + (c.TILE_SIZE / 2))
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)

        # Makes it so the enemies come out randomly
        random.shuffle(self.enemy_list)

    def draw(self, surface):
        surface.blit(self.image, (0, 0)) # Cordnates to start drawing from
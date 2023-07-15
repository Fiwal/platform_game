import pygame
from pygame.locals import *

import json

from static_objects import StaticObject
from enemy import Enemy
from player import Player
from objects import Object
from grass import Grass

from structures import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 200)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


def open_json(file):

    with open(file, 'r') as f:
        return json.load(f)


class Game:

    def __init__(self, width, height):

        pygame.init()

        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        # init game:

        self.run = True

        self.GRAVITY = 1
        self.FPS = 60

        self.player_on_the_ground = False
        self.is_jump = False

        pygame.display.set_caption('platform_game')

        self.background = StaticObject(0, 0, self.width, self.height, self, "images/background.png")

        self.size_of_blocks = 70

        self.objects = []
        self.background_objects = []
        self.grass = []

        self.player = Player(350, 300, 50, 70, self)
        self.list_of_enemies = []

        self.explosions = []

        self.offsetX = 0

        self.level = 1

    def add_enemies(self):

        enemies = open_json(f'levels/level_{self.level}/enemies.json')

        for i in enemies['elements']:
            self.list_of_enemies.append(Enemy(i['x'], i['y'], 50, 40, self, i['start_vel_x']))

    def add_objects(self):

        grounds = open_json(f'levels/level_{self.level}/ground.json')

        for i in grounds['elements']:
            self.add_ground(i['start_x'], i['end_x'], i['start_y'],  i['end_y'])

        structures = open_json(f'levels/level_{self.level}/structures.json')

        for i in structures['elements']:
            self.add_structures(i['number_of_structure'], i['x'], i['y'])

        platforms = open_json(f'levels/level_{self.level}/platforms.json')

        for i in platforms['elements']:
            self.objects.append(Object(i['x'], i['y'], 210, 35, self, "images/blocks_and_platforms/platform.png"))

        grass = open_json(f'levels/level_{self.level}/grass.json')

        for i in grass['elements']:
            self.add_grass(i['start_x'], i['end_x'], i['y'])

        trees = open_json(f'levels/level_{self.level}/trees.json')

        for i in trees['elements']:
            if i['size'] == 'large':
                self.background_objects.append(Object(i['x'], i['y'], 263, 350, self, "images/nature/tree.png"))
            elif i['size'] == 'small':
                self.background_objects.append(Object(i['x'], i['y'], 211, 280, self, "images/nature/tree.png"))

        mushrooms = open_json(f'levels/level_{self.level}/mushrooms.json')

        for i in mushrooms['elements']:
            self.background_objects.append(Object(i['x'], i['y'], self.size_of_blocks, self.size_of_blocks, self,
                                                  "images/nature/mushroom.png"))

        plants = open_json(f'levels/level_{self.level}/plants.json')

        for i in plants['elements']:
            self.background_objects.append(Object(i['x'], i['y'], 70, 140, self, "images/nature/plant.png"))

    def add_ground(self, start_x, end_x, start_y, end_y):

        for i in range(start_x, end_x):
            self.objects.append(Object(i, start_y, self.size_of_blocks,
                                self.size_of_blocks, self, "images/blocks_and_platforms/ground/ground1.png"))
            for j in range(start_y + 1, end_y):
                self.objects.append(Object(i, j, self.size_of_blocks,
                                    self.size_of_blocks, self, "images/blocks_and_platforms/ground/ground2.png"))

    def add_structures(self, number_of_structure, start_x, start_y):

        for i in range(len(all_structures[number_of_structure])):

            for j in range(len(all_structures[number_of_structure][i])):

                if all_structures[number_of_structure][i][j] == "B1":
                    self.objects.append(Object(start_x + j, start_y + i, self.size_of_blocks,
                                               self.size_of_blocks, self, "images/blocks_and_platforms/block1.png"))
                elif all_structures[number_of_structure][i][j] == "G1":
                    self.objects.append(Object(start_x + j, start_y + i, self.size_of_blocks,
                                               self.size_of_blocks, self,
                                               "images/blocks_and_platforms/ground/ground1.png"))
                elif all_structures[number_of_structure][i][j] == "G2":
                    self.objects.append(Object(start_x + j, start_y + i, self.size_of_blocks,
                                               self.size_of_blocks, self,
                                               "images/blocks_and_platforms/ground/ground2.png"))

    def add_grass(self, start_x, end_x, y):

        for i in range(start_x, end_x):

            self.grass.append(Grass(i, y, self.size_of_blocks, self.size_of_blocks, self))

    def main(self):

        self.add_objects()
        self.add_enemies()

        while self.run:

            if self.player.y - self.player.height > self.width:
                self.player.lives = 0

            self.check_if_close_game()
            self.move_player()
            self.update()
            self.solve_collisions_with_enemies()

            if self.player.lives == 0:
                self.run = False

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()

    def move_player(self):

        keys = pygame.key.get_pressed()

        self.solve_collision_and_draw()
        if self.player_on_the_ground or self.is_jump:
            if keys[K_d]:
                self.player.move(0.7)
            elif keys[K_a]:
                self.player.move(-0.7)

        if not self.player_on_the_ground:
            self.player.y_Vel = 13

        if self.player_on_the_ground:

            if keys[K_w]:

                self.player.y_jump = -31
                self.is_jump = True
                self.player_on_the_ground = False

        if self.is_jump:

            self.player.jump()

        self.player_on_the_ground = False

    def check_if_close_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                break

    def update(self):

        self.offsetX = self.player.x - self.width / 4
        self.player.update()

        for i in self.list_of_enemies:
            i.update()

        for i in self.grass:
            if i.x - self.offsetX > -300:
                if i.x - self.offsetX < self.width:
                    i.update()

        for i in self.explosions:
            i.update()
            if i.end_explosion:
                self.explosions.pop(self.explosions.index(i))

    def solve_collision_and_draw(self):

        self.window.fill(BLUE)
        self.background.draw()

        for i in self.objects:

            if i.x - self.offsetX > -300:
                if i.x - self.offsetX < self.width:

                    self.solve_collisions(i)
                    i.draw()

        for i in self.background_objects:
            if i.x - self.offsetX > -300:
                if i.x - self.offsetX < self.width:
                    i.draw()

        for i in self.grass:
            if i.x - self.offsetX > -300:
                if i.x - self.offsetX < self.width:
                    i.draw()

        for i in self.list_of_enemies:
            if i.x - self.offsetX > -300:
                if i.x - self.offsetX < self.width:
                    i.draw()

        self.player.draw()

        for i in self.explosions:
            i.draw()

        self.player.draw_hearts()

    def solve_collisions_with_enemies(self):

        for i in self.list_of_enemies:

            if not i.explosion:

                if self.player.rect.colliderect(i.rect):

                    i.start_ticks_to_explosion = pygame.time.get_ticks()
                    i.start_ticks_for_animation = pygame.time.get_ticks()
                    i.explosion = True

            self.solve_collisions(i)

    def solve_collisions(self, i):

        if not self.player.y_Vel == 0:
            if self.player.y + self.player.height > i.y + 1:
                if self.player.x + self.player.width > i.x and self.player.x < i.x + i.width:
                    if self.player.y + self.player.height < i.y + i.height / 2:
                        self.player.y = i.y - self.player.height
                        self.player_on_the_ground = True

            if self.player.y < i.y + i.height:
                if self.player.x + self.player.width > i.x and self.player.x < i.x + i.width:
                    if self.player.y > i.y + i.height - i.height / 2:
                        self.player.y = i.y + i.height
                        self.player.y_jump = -5
                        self.player.y_Vel = 0

        if not self.player.x_Vel == 0:
            if self.player.x + self.player.width > i.x:
                if self.player.y + self.player.height > i.y and self.player.y < i.y + i.height:
                    if self.player.x + self.player.width < i.x + 10:
                        self.player.x_Vel = 0
                        self.player.x = i.x - self.player.width

            if self.player.x < i.x + i.width:
                if self.player.y + self.player.height > i.y and self.player.y < i.y + i.height:
                    if self.player.x > i.x + i.width - 10:
                        self.player.x_Vel = 0
                        self.player.x = i.x + i.width


if __name__ == "__main__":

    game = Game(1500, 700)
    game.main()

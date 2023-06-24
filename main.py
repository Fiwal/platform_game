import pygame
from pygame.locals import *
from enemy import Enemy
from player import Player
from objects import Object
from structures import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 200)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


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
        self.FPS = 110

        self.player_on_the_ground = False
        self.is_jump = False

        pygame.display.set_caption('platform_game')

        self.width_and_height_of_blocks = 70

        self.objects = []
        self.player = Player(self.width / 4, 10, 50, 70, self)
        self.list_of_enemies = []

        self.offsetX = 0

    def add_enemies(self):

        self.list_of_enemies.append(Enemy(1900, 500, 50, 40, self, -3))
        self.list_of_enemies.append(Enemy(2500, 500, 50, 40, self, 3))
        self.list_of_enemies.append(Enemy(6300, 500, 50, 40, self, 3))

    def add_objects(self):

        self.add_ground(-8, 20, 8, 10)
        self.add_ground(22, 40, 8, 10)
        self.add_ground(40, 43, 7, 10)
        self.add_ground(43, 50, 6, 10)
        self.add_ground(67, 80, 8, 10)
        self.add_ground(82, 106, 8, 10)
        self.add_ground(112, 120, 8, 10)

        self.add_structures(structure1, 16, 5)
        self.add_structures(structure2, 22, 5)
        self.add_structures(structure3, 76, 4)
        self.add_structures(structure4, 82, 4)
        self.add_structures(structure5, 100, 4)

        self.objects.append(Object(52, 6, 210, 35, self, "images/platform.png"))
        self.objects.append(Object(57, 5, 210, 35, self, "images/platform.png"))
        self.objects.append(Object(62, 7, 210, 35, self, "images/platform.png"))
        self.objects.append(Object(72, 6, 210, 35, self, "images/platform.png"))
        self.objects.append(Object(107.5, 4, 210, 35, self, "images/platform.png"))

    def add_ground(self, start_y, end_y, start_x, end_x):

        for i in range(start_y, end_y):
            self.objects.append(Object(i, start_x, self.width_and_height_of_blocks,
                                       self.width_and_height_of_blocks, self, "images/ground1.png"))
            for j in range(start_x + 1, end_x):
                self.objects.append(Object(i, j, self.width_and_height_of_blocks,
                                           self.width_and_height_of_blocks, self, "images/ground2.png"))

    def add_structures(self, structure, start_x, start_y):

        for i in range(len(structure)):

            for j in range(len(structure[i])):

                if structure[i][j] == "B1":
                    self.objects.append(Object(start_x + j, start_y + i, self.width_and_height_of_blocks,
                                               self.width_and_height_of_blocks, self, "images/block1.png"))

    def main(self):

        self.add_objects()
        self.add_enemies()

        while self.run:

            self.check_if_close_game()
            self.move_player()
            self.update()
            self.solve_collisions_with_enemies()

            if self.player.y - self.player.height > self.width:
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

                self.player.y_jump = -29.5
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

    def solve_collision_and_draw(self):

        self.window.fill(BLUE)

        for i in self.objects:

            if i.y > self.width / 4 - 200:
                if i.y < self.width / 4 + 200:
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

            if i.y > -1:
                if i.y < self.width + 1:
                    i.draw()

        for i in self.list_of_enemies:
            i.draw()

        self.player.draw()

    def solve_collisions_with_enemies(self):

        for i in self.list_of_enemies:

            if self.player.rect.colliderect(i.rect):

                self.run = False


if __name__ == "__main__":

    game = Game(1500, 700)
    game.main()

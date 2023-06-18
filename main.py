import pygame
from pygame.locals import *
from player import Player
from block import Block
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
        self.is_jump = False
        self.run = True
        self.player_on_the_ground = False
        self.clock = pygame.time.Clock()
        self.width_and_height_of_blocks = 70
        self.objects = []
        self.offsetX = 0
        self.jump_left = False
        self.jump_right = False
        pygame.display.set_caption('platform_game')

        self.player = Player(self.width / 4, 10, 50, 70, self)

    def make_blocks(self):

        self.make_ground(-8, 20, 8, 10)
        self.make_ground(22, 40, 8, 10)
        self.make_ground(40, 43, 7, 10)
        self.make_ground(43, 50, 6, 10)
        self.make_structures(structure1, 16, 5)
        self.make_structures(structure2, 22, 5)
        self.objects.append(Block(52, 6, 210, 35, self, "images/platform.png"))
        self.objects.append(Block(57, 5, 210, 35, self, "images/platform.png"))
        self.objects.append(Block(62, 7, 210, 35, self, "images/platform.png"))
        self.make_ground(67, 80, 8, 10)
        self.make_structures(structure3, 76, 4)
        self.objects.append(Block(72, 6, 210, 35, self, "images/platform.png"))
        self.make_structures(structure4, 82, 4)
        self.make_ground(82, 100, 8, 10)

    def make_ground(self, start_y, end_y, start_x, end_x):

        for i in range(start_y, end_y):
            self.objects.append(Block(i, start_x, self.width_and_height_of_blocks,
                                      self.width_and_height_of_blocks, self, "images/ground1.png"))
            for j in range(start_x + 1, end_x):
                self.objects.append(Block(i, j, self.width_and_height_of_blocks,
                                          self.width_and_height_of_blocks, self, "images/ground2.png"))

    def make_structures(self, structure, start_x, start_y):

        for i in range(len(structure)):

            for j in range(len(structure[i])):

                if structure[i][j] == "B1":
                    self.objects.append(Block(start_x + j, start_y + i, self.width_and_height_of_blocks,
                                              self.width_and_height_of_blocks, self, "images/block1.png"))

    def main(self):

        self.make_blocks()

        while self.run:

            if self.player.y - self.player.height > self.width:
                self.run = False
            self.update()
            self.move_player()
            self.check_if_close_game()
            self.draw()

        pygame.quit()

    def move_player(self):

        keys = pygame.key.get_pressed()

        self.check_collision()
        if self.player_on_the_ground:
            if keys[K_d]:
                self.player.move(1.2)
            elif keys[K_a]:
                self.player.move(-1.2)

        if not self.player_on_the_ground:
            self.player.y_Vel = 13

        if self.player_on_the_ground:

            if keys[K_w]:
                if keys[K_d]:
                    self.jump_right = True
                elif keys[K_a]:
                    self.jump_left = True
                self.player.y_jump = -29.5
                self.is_jump = True
                self.player_on_the_ground = False

        if self.is_jump:

            self.player.jump()

        if not self.player_on_the_ground:

            if self.jump_right:
                self.player.move(1.2)
            elif self.jump_left:
                self.player.move(-1.2)

        self.player_on_the_ground = False

    def check_if_close_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                break

    def draw(self):

        self.window.fill(BLUE)

        for i in self.objects:
            if i.y > -1:
                if i.y < self.width + 1:
                    i.draw()

        self.player.draw()

        self.clock.tick(120)
        pygame.display.flip()

    def update(self):

        self.offsetX = self.player.x - self.width / 4
        self.player.update()

    def check_collision(self):

        for object_to_check_collision in self.objects:
            if object_to_check_collision.y > self.width / 4 - 200:
                if object_to_check_collision.y < self.width / 4 + 200:
                    if not self.player.y_Vel == 0:
                        if self.player.y + self.player.height > object_to_check_collision.y + 1:
                            if self.player.x + self.player.width > object_to_check_collision.x and \
                                    self.player.x < object_to_check_collision.x + object_to_check_collision.width:
                                if self.player.y + self.player.height < object_to_check_collision.y + \
                                        object_to_check_collision.height / 2:
                                    self.player.y = object_to_check_collision.y - self.player.height
                                    self.player_on_the_ground = True
                                    self.jump_left = False
                                    self.jump_right = False
                                    self.player.update_rect()

                        if self.player.y < object_to_check_collision.y + object_to_check_collision.height:
                            if self.player.x + self.player.width > object_to_check_collision.x and \
                                    self.player.x < object_to_check_collision.x + object_to_check_collision.width:
                                if self.player.y > object_to_check_collision.y + object_to_check_collision.height - \
                                        object_to_check_collision.height / 2:
                                    self.player.y = object_to_check_collision.y + object_to_check_collision.height
                                    self.player.y_jump = -5
                                    self.player.y_Vel = 0
                                    self.player.update_rect()

                    if not self.player.x_Vel == 0:
                        if self.player.x + self.player.width > object_to_check_collision.x:
                            if self.player.y + self.player.height > object_to_check_collision.y and \
                                    self.player.y < object_to_check_collision.y + object_to_check_collision.height:
                                if self.player.x + self.player.width < object_to_check_collision.x + 10:
                                    self.player.x_Vel = 0
                                    self.player.x = object_to_check_collision.x - self.player.width
                                    self.player.update_rect()

                        if self.player.x < object_to_check_collision.x + object_to_check_collision.width:
                            if self.player.y + self.player.height > object_to_check_collision.y and \
                                    self.player.y < object_to_check_collision.y + object_to_check_collision.height:
                                if self.player.x > object_to_check_collision.x + object_to_check_collision.width - 10:
                                    self.player.x_Vel = 0
                                    self.player.x = object_to_check_collision.x + object_to_check_collision.width
                                    self.player.update_rect()


if __name__ == "__main__":

    game = Game(1500, 700)
    game.main()

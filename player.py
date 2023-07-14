import pygame
from pygame import Rect
from game_object import GameObject


class Player(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, game):

        super().__init__(x, y, width, height, game, "images/player/player.png")

        self.game = game
        self.x_Vel = 0
        self.y_jump = 0
        self.y_Vel = game.GRAVITY

        self.start_lives = 4
        self.lives = self.start_lives

        self.heart_image = pygame.transform.scale(pygame.image.load("images/heart.png"), (52.5, 45))
        self.heart2_image = pygame.transform.scale(pygame.image.load("images/heart2.png"), (52.5, 45))

    def jump(self):

        if not self.y_jump > 0:
            self.y_jump += 1

        else:
            self.game.is_jump = False

    def update(self):

        self.x_Vel *= 0.90

        self.x += self.x_Vel

        self.y += self.y_Vel + self.y_jump

        self.update_rect()

    def move(self, x):

        self.x_Vel += x

    def update_rect(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw_hearts(self):

        for i in range(self.start_lives):
            self.game.window.blit(self.heart2_image, (i * 70 + 30, 30))

        for i in range(self.lives):
            self.game.window.blit(self.heart_image, (i * 70 + 30, 30))

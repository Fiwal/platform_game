import pygame
from pygame import Rect


class GameObject:

    def __init__(self, x, y: int, width: int, height: int, game, image_src):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.img = pygame.transform.scale(pygame.image.load(image_src), (self.width, self.height))

    def draw(self):

        drawX = self.x - self.game.offsetX
        self.game.window.blit(self.img, (drawX, self.y))

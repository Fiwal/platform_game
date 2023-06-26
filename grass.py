import pygame
from game_object import GameObject


class Grass(GameObject):

    def __init__(self, x, y: int, width: int, height: int, game):

        self.type_of_grass = 1
        self.image = f"images/grass{self.type_of_grass}.png"

        super().__init__(x * game.width_and_height_of_blocks, y * game.width_and_height_of_blocks,
                         width, height, game, self.image)

        self.start_ticks = pygame.time.get_ticks()

    def update(self):

        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

        if seconds > 0.2:

            self.start_ticks = pygame.time.get_ticks()

            if self.type_of_grass == 1:
                self.image = f"images/grass{self.type_of_grass}.png"
                self.img = pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height))
                self.type_of_grass = 2

            elif self.type_of_grass == 2:
                self.image = f"images/grass{self.type_of_grass}.png"
                self.img = pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height))
                self.type_of_grass = 1


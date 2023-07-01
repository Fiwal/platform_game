import random
from pygame import Rect

from game_object import GameObject


class Rubble(GameObject):

    def __init__(self, x, y, width, height, x_vel, y_vel, image, game):

        super().__init__(x, y, width, height, game, image)

        self.x_vel = x_vel
        self.y_vel = y_vel
        self.game = game
        self.time_to_delete = random.randint(10, 30)
        self.on_the_ground = False

    def update(self):

        if not self.y_vel > -1:
            self.y_vel *= 0.999

        if not self.on_the_ground:
            self.y_vel += self.game.GRAVITY

        self.y += self.y_vel

        self.x_vel *= 0.98
        self.x += self.x_vel

        self.rect = Rect(self.x, self.y, self.height, self.width)

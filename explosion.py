import random
import pygame
from pygame import Rect
from game_object import GameObject


class Smoke(GameObject):

    def __init__(self, x, y, width, height, x_vel, y_vel, image, game):

        super().__init__(x, y, width, height, game, image)

        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):

        if not self.y_vel > 0:
            self.y_vel += 0.1
            self.y_vel *= 0.99
            self.y += self.y_vel

        self.x_vel *= 0.99
        self.x += self.x_vel


class Rubble(GameObject):

    def __init__(self, x, y, width, height, x_vel, y_vel, image, game):

        super().__init__(x, y, width, height, game, image)

        self.x_vel = x_vel
        self.y_vel = y_vel
        self.game = game
        self.time_to_delete = random.randint(10, 30)

    def update(self):

        if not self.y_vel > 0:
            self.y_vel += 0.15

        self.y_vel += self.game.GRAVITY / 10

        self.y += self.y_vel

        self.x_vel *= 0.99
        self.x += self.x_vel

        self.rect = Rect(self.x, self.y, self.height, self.width)


class Zone(GameObject):

    def __init__(self, x, y, width, height, image, game):

        self.start_x = x
        self.start_y = y

        self.plus_size = 20

        self.x = self.start_x - width / 2
        self.y = self.start_y - height / 2
        self.image = image

        self.time_to_delete = 0.7

        super().__init__(self.x, self.y, width, height, game, image)

    def update(self):

        if not self.plus_size < 0:
            self.width += self.plus_size
            self.height += self.plus_size

        self.x = self.start_x - self.width / 2
        self.y = self.start_y - self.height / 2
        self.img = self.img = pygame.transform.scale(pygame.image.load(self.image), (self.width, self.height))

        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.plus_size -= 0.3


class Explosion:

    def __init__(self, x, y, game):

        self.x = x
        self.y = y

        self.window = game.window
        self.game = game

        self.smoke = []
        self.rubble = []

        self.danger_zone = []
        self.danger_zone.append(Zone(x, y, 50, 50, "images/Elements_to_explosion/danger_zone.png", self.game))

        self.add_smoke_and_rubble()

        self.start_explosion = pygame.time.get_ticks()
        self.end_explosion = False

    def add_smoke_and_rubble(self):

        for i in range(30):
            random_x_vel = random.uniform(-4, 4)
            random_y_vel = random.uniform(-9, -13)
            random_size = random.randint(60, 100)
            random_image = random.randint(1, 3)
            self.smoke.append(Smoke(self.x, self.y, random_size, random_size, random_x_vel,
                              random_y_vel, f"images/Elements_to_explosion/smoke_{random_image}.png", self.game))

        for i in range(40):
            random_x_vel = random.uniform(-5, 5)
            random_y_vel = random.uniform(-9, -13)
            random_size = random.randint(10, 20)
            random_image = random.randint(1, 3)
            self.rubble.append(Rubble(self.x, self.y, random_size, random_size, random_x_vel,
                               random_y_vel, f"images/Elements_to_explosion/rubble_{random_image}.png", self.game))

    def update(self):

        for i in self.smoke:
            i.update()
            if i.y_vel > 0:
                self.smoke.pop(self.smoke.index(i))
                i.x_vel = 0

        seconds = (pygame.time.get_ticks() - self.start_explosion) / 1000
        for i in self.rubble:
            i.update()
            if i.time_to_delete < seconds:
                self.rubble.pop(self.rubble.index(i))

            self.solve_collisions(i)

        for i in self.danger_zone:
            i.update()
            if i.time_to_delete < seconds:
                self.danger_zone.pop(self.danger_zone.index(i))

        if len(self.rubble) == 0 and len(self.smoke) == 0:
            self.end_explosion = True

    def draw(self):

        for i in self.danger_zone:
            i.draw()

        for i in self.smoke:
            i.draw()

        for i in self.rubble:
            i.draw()

    def solve_collisions(self, j):

        for i in self.game.objects:

            if not j.y_vel == 0:
                if j.y + j.height > i.y + 1:
                    if j.x + j.width > i.x and j.x < i.x + i.width:
                        if j.y + j.height < i.y + i.height:
                            j.y = i.y - j.height
                            j.y_vel = 0

            if not j.x_vel == 0:
                if j.x + j.width > i.x:
                    if j.y + j.height > i.y and j.y < i.y + i.height:
                        if j.x + j.width < i.x + 10:
                            j.x_vel = 0
                            j.x = i.x - j.width

                if j.x < i.x + i.width:
                    if j.y + j.height > i.y and j.y < i.y + i.height:
                        if j.x > i.x + i.width - 10:
                            j.x_vel = 0
                            j.x = i.x + i.width

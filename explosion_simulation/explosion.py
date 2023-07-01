import random
import pygame

from explosion_simulation.rubble import Rubble
from explosion_simulation.smoke import Smoke


class Explosion:

    def __init__(self, x, y, game):

        self.x = x
        self.y = y

        self.window = game.window
        self.game = game

        self.smoke = []
        self.rubble = []

        self.add_smoke_and_rubble()

        self.start_explosion = pygame.time.get_ticks()
        self.end_explosion = False

    def add_smoke_and_rubble(self):

        for i in range(30):
            random_x_vel = random.uniform(-6, 6)
            random_y_vel = random.uniform(-9, -13)
            random_size = random.randint(60, 100)
            random_image = random.randint(1, 3)
            self.smoke.append(Smoke(self.x, self.y, random_size, random_size, random_x_vel,
                              random_y_vel, f"images/Elements_to_explosion/smoke_{random_image}.png", self.game))

        for i in range(30):
            random_x_vel = random.uniform(-8, 8)
            random_y_vel = random.uniform(-15, -20)
            random_size = random.randint(15, 20)
            random_image = random.randint(1, 3)
            self.rubble.append(Rubble(self.x, self.y, random_size, random_size, random_x_vel,
                               random_y_vel, f"images/Elements_to_explosion/rubble_{random_image}.png", self.game))

    def update(self):

        for i in self.smoke:
            i.update()
            if i.y_vel > -1:
                self.smoke.pop(self.smoke.index(i))
                i.x_vel = 0

        seconds = (pygame.time.get_ticks() - self.start_explosion) / 1000
        for i in self.rubble:
            i.update()
            if i.time_to_delete < seconds:
                self.rubble.pop(self.rubble.index(i))

            self.solve_collisions(i)

        if len(self.rubble) == 0 and len(self.smoke) == 0:
            self.end_explosion = True

    def draw(self):

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
                            j.on_the_ground = True

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

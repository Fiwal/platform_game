import random
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

    def update(self):

        if not self.y_vel > 0:
            self.y_vel += 0.1
            self.y_vel *= 0.99

        self.y_vel += self.game.GRAVITY * 0.076

        self.y += self.y_vel

        self.x_vel *= 0.99
        self.x += self.x_vel

        self.rect = Rect(self.x, self.y, self.height, self.width)


class Explosion:

    def __init__(self, x, y, game):

        self.x = x
        self.y = y

        self.window = game.window
        self.game = game

        self.smoke = []
        self.rubble = []

        self.add_smoke_and_rubble()

        self.end_explosion = False

    def add_smoke_and_rubble(self):

        for i in range(20):
            random_x_vel = random.uniform(-4, 4)
            random_y_vel = random.uniform(-9, -13)
            random_size = random.randint(60, 90)
            random_image = random.randint(1, 3)
            self.smoke.append(Smoke(self.x, self.y, random_size, random_size, random_x_vel,
                              random_y_vel, f"images/Elements_to_explosion/smoke_{random_image}.png", self.game))

        for i in range(40):
            random_x_vel = random.uniform(-3.5, 3.5)
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

        for i in self.rubble:
            i.update()

        self.solve_collisions()

        if len(self.rubble) == 0 and len(self.smoke) == 0:
            self.end_explosion = True

    def draw(self):

        for i in self.smoke:
            i.draw()

        for i in self.rubble:
            i.draw()

    def solve_collisions(self):

        for i in self.rubble:

            for j in self.game.objects:

                if i.rect.colliderect(j.rect):

                    self.rubble.pop(self.rubble.index(i))
                    break

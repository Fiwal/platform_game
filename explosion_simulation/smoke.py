from game_object import GameObject


class Smoke(GameObject):

    def __init__(self, x, y, width, height, x_vel, y_vel, image, game):

        super().__init__(x, y, width, height, game, image)

        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):

        if not self.y_vel > 0:
            self.y_vel *= 0.975
            self.y += self.y_vel

        self.x_vel *= 0.99
        self.x += self.x_vel
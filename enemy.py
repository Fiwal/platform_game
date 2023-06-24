from pygame import Rect
from game_object import GameObject


class Enemy(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, game, start_x_Vel):

        super().__init__(x, y, width, height, game, "images/enemy.png")

        self.game = game
        self.x_Vel = start_x_Vel
        self.y_Vel = 20

    def update(self):

        self.x += self.x_Vel
        self.y += self.y_Vel
        self.solve_collision()
        self.update_rect()

    def update_rect(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def solve_collision(self):

        for i in self.game.objects:

            if not self.y_Vel == 0:
                if self.y + self.height > i.y + 1:
                    if self.x + self.width > i.x and self.x < i.x + i.width:
                        if self.y + self.height < i.y + i.height:
                            self.y = i.y - self.height

            if not self.x_Vel == 0:
                if self.x + self.width > i.x:
                    if self.y + self.height > i.y and self.y < i.y + i.height:
                        if self.x + self.width < i.x + 10:
                            self.x_Vel = -3

                if self.x < i.x + i.width:
                    if self.y + self.height > i.y and self.y < i.y + i.height:
                        if self.x > i.x + i.width - 10:
                            self.x_Vel = 3

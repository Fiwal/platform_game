import pygame
from pygame import Rect
from game_object import GameObject
from explosion_simulation.explosion import Explosion


class Enemy(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, game, x_speed):

        super().__init__(x, y, width, height, game, "images/enemy/enemy.png")

        self.game = game
        self.x_Vel = x_speed
        self.y_Vel = 20
        self.explosion = False
        self.start_ticks_to_explosion = 0
        self.start_ticks_for_animation = 0
        self.explosion_type_of_enemy = 1

    def update(self):

        if self.explosion:

            self.explosion_enemy()

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

    def explosion_enemy(self):

        self.before_explosion_animation()

        self.x_Vel = 0
        seconds = (pygame.time.get_ticks() - self.start_ticks_to_explosion) / 1000

        if seconds > 0.3:
            self.game.explosions.append(Explosion(self.x + self.width / 2, self.y, self.game))
            self.game.list_of_enemies.pop(self.game.list_of_enemies.index(self))
            self.game.player.lives -= 1

    def before_explosion_animation(self):

        seconds = (pygame.time.get_ticks() - self.start_ticks_for_animation) / 1000

        if seconds > 0.05:
            if self.explosion_type_of_enemy == 1:

                self.img = pygame.transform.scale(pygame.image.load("images/enemy/enemy.png"),
                                                  (self.width, self.height))
                self.explosion_type_of_enemy = 2

            elif self.explosion_type_of_enemy == 2:
                self.img = pygame.transform.scale(pygame.image.load("images/enemy/explosion_enemy.png"),
                                                  (self.width, self.height))
                self.explosion_type_of_enemy = 1

            self.start_ticks_for_animation = pygame.time.get_ticks()

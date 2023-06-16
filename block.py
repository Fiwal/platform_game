from game_object import GameObject


class Block(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, game, image):

        super().__init__(x * width, y * height, width, height, game, image)

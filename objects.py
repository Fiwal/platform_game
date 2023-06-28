from game_object import GameObject


class Object(GameObject):

    def __init__(self, x, y: int, width: int, height: int, game, image):

        super().__init__(x * game.size_of_blocks, y * game.size_of_blocks,
                         width, height, game, image)

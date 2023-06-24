from game_object import GameObject


class Object(GameObject):

    def __init__(self, x, y: int, width: int, height: int, game, image):

        super().__init__(x * game.width_and_height_of_blocks, y * game.width_and_height_of_blocks,
                         width, height, game, image)

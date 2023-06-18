from game_object import GameObject


class Block(GameObject):

    def __init__(self, x: int, y: int, width: int, height: int, game, image):

        super().__init__(x * game.width_and_height_of_blocks, y * game.width_and_height_of_blocks,
                         width, height, game, image)

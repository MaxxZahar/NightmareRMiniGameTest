# Основные элементы на карте - фишки и блоки.
class FieldElement:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Block(FieldElement):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.entity = 'block'

    def __str__(self):
        return f'{self.entity} at ({self.x}, {self.y})'

    @classmethod
    def create_block(cls, point: tuple):
        return cls(point[0], point[1])


class Token(FieldElement):
    def __init__(self, x: int, y: int, suit: str):
        super().__init__(x, y)
        self.entity = 'token'
        self.suit = suit

    def __str__(self):
        return f'{self.suit} {self.entity} at ({self.x}, {self.y})'

    @classmethod
    def create_token(cls, point: tuple, suit: str):
        return cls(point[0], point[1], suit)

    def move(self, direction: str):
        match direction:
            case 'up':
                self.x -= 1
            case 'down':
                self.x += 1
            case 'left':
                self.y -= 1
            case 'right':
                self.y += 1

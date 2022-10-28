from field_elements import Block, Token
from suits import suits
import random

dimension = (5, 5)
number_of_suits = len(suits)
number_of_tokens = 5
number_of_blocks = 6


class FieldMap:
    def __init__(self, dimension: tuple):
        self.number_of_rows = dimension[0]
        self.number_of_columns = dimension[1]
        self.map = [0 for _ in range(dimension[0] * dimension[1])]

    def __str__(self):
        return f'{self.map}'

    @classmethod
    def create_empty_map(cls, dimension: tuple):
        return cls(dimension)

    @classmethod
    def create_random_map(cls, dimension: tuple, number_of_suits: int, number_of_tokens: int, number_of_blocks: int):
        m = cls(dimension)
        if number_of_suits * number_of_tokens + number_of_blocks >= dimension[0] * dimension[1]:
            raise ValueError('Excessive field content')
        elements = []
        for suit in suits:
            tokens = [suit for _ in range(number_of_tokens)]
            elements.extend(tokens)
        blocks = ['block' for _ in range(number_of_blocks)]
        elements.extend(blocks)
        number_of_spaces = dimension[0] * dimension[1] - \
            (number_of_suits * number_of_tokens + number_of_blocks)
        spaces = [0 for _ in range(number_of_spaces)]
        elements.extend(spaces)
        random.shuffle(elements)
        for i, el in enumerate(elements):
            if el:
                if el == 'block':
                    elements[i] = Block.create_block(
                        d1tod2(i, m.number_of_columns))

                else:
                    elements[i] = Token.create_token(
                        d1tod2(i, m.number_of_columns), el)
        m.map = elements
        return m


def d1tod2(x: int, number_of_columns: int):
    return (x % number_of_columns, x // number_of_columns)


m = FieldMap.create_random_map(
    dimension, number_of_suits, number_of_tokens, number_of_blocks)
print(m)

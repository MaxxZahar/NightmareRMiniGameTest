from field_elements import Block, Token
from suits import suits
from settings import settings
from ut_funcs import d1tod2, d2tod1
import random


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
        elements = [0 for _ in range(dimension[0] * dimension[1])]
        spaces = list(range(dimension[0] * dimension[1]))
        for _ in range(number_of_blocks):
            el = random.choice(settings['acceptable_blocks'])
            i = d2tod1(el, m.number_of_columns)
            elements[i] = Block.create_block(el)
            spaces.remove(i)
            settings['acceptable_blocks'].remove(el)
        for suit in suits:
            for _ in range(number_of_tokens):
                i = random.choice(spaces)
                elements[i] = Token.create_token(
                    d1tod2(i, m.number_of_columns), suit['name'])
                spaces.remove(i)
        m.map = elements
        return m


class Field:
    def __init__(self, settings):
        self.settings = settings
        self.map = FieldMap.create_random_map(
            settings['dimension'], settings['number_of_suits'], settings['number_of_tokens'], settings['number_of_blocks'])

    def __str__(self):
        return f'Начальное поле {self.map}'

    @classmethod
    def create_field(cls):
        return cls(settings)


# f = Field(settings)
# print(f)

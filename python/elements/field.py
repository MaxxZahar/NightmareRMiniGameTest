from field_elements import Block, Token
from suits import suits
from settings import settings
from ut_funcs import d1tod2, d2tod1
import random

# Класс карты


class FieldMap:
    def __init__(self, dimension: tuple):
        self.number_of_rows = dimension[0]
        self.number_of_columns = dimension[1]
        self.map = [0 for _ in range(dimension[0] * dimension[1])]

    def __str__(self):
        return f'{self.map}'

    def __iter__(self):
        return iter(self.map)

    def __len__(self):
        return len(self.map)

    @classmethod
    def create_empty_map(cls, dimension: tuple):
        return cls(dimension)

    # Метод для генерирования случайной карты.
    @classmethod
    def create_random_map(cls, dimension: tuple, number_of_suits: int, number_of_tokens: int, number_of_blocks: int):
        m = cls(dimension)
        if number_of_suits * number_of_tokens + number_of_blocks >= dimension[0] * dimension[1]:
            raise ValueError('Excessive field content')
        elements = [0 for _ in range(dimension[0] * dimension[1])]
        spaces = list(range(dimension[0] * dimension[1]))
        # Генерируем блоки
        block_scheme = {}
        for _ in range(number_of_blocks):
            el = random.choice(settings['acceptable_blocks'])
            i = d2tod1(el, m.number_of_columns)
            elements[i] = Block.create_block(el)
            if block_scheme.get(el[0]):
                block_scheme[el[0]] += 1
            else:
                block_scheme[el[0]] = 1
            spaces.remove(i)
            settings['acceptable_blocks'].remove(el)
            # Проверяем, что есть дырки в столбце блоков. Для произвольного расположения этого не достаточно, но для дефолтного вполне.
            if block_scheme[el[0]] == dimension[0] - settings['min_block_spaces']:
                settings['acceptable_blocks'] = [
                    block for block in settings['acceptable_blocks'] if block[0] != el[0]]
        # Генерируем фишки
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

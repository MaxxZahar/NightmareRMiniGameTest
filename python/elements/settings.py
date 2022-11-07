from suits import suits
import random


def get_token_columns(number_of_columns: int, number_of_suits: int, manual=True):
    if manual:
        lst = [0, 2, 4]
        if len(lst) != number_of_suits:
            raise ValueError('Wrong number of token columns')
        random.shuffle(lst)
        return lst
    else:
        lst = list(range(number_of_columns))
        random.shuffle(lst)
        return lst[:number_of_suits]


settings = {
    'dimension': (5, 5),
    'number_of_suits': len(suits),
    'number_of_tokens': 5,
    'number_of_blocks': 6,
    'min_block_spaces': 2,
}

settings['token_columns'] = get_token_columns(
    settings['dimension'][1], settings['number_of_suits'])


def get_acceptable_blocks(dimension: tuple, token_columns: list):
    number_of_rows = dimension[0]
    number_of_columns = dimension[1]
    result = []
    for i in range(number_of_columns):
        if i not in token_columns:
            for j in range(number_of_rows):
                result.append((i, j))
    return result


settings['acceptable_blocks'] = get_acceptable_blocks(
    settings['dimension'], settings['token_columns'])

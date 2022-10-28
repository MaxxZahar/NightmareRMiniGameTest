from suits import suits
import random


def get_token_columns(number_of_columns: int, number_of_suits: int):
    lst = list(range(number_of_columns))
    random.shuffle(lst)
    return lst[:number_of_suits]


settings = {
    'dimension': (5, 5),
    'number_of_suits': len(suits),
    'number_of_tokens': 5,
    'number_of_blocks': 6,
}

settings['token_columns'] = get_token_columns(
    settings['dimension'][1], settings['number_of_suits'])

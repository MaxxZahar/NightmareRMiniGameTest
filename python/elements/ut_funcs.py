def d1tod2(x: int, number_of_columns: int):
    return (x % number_of_columns, x // number_of_columns)


def d2tod1(x: tuple, number_of_columns: int):
    return x[0] + x[1] * number_of_columns


def get_suit_index(suit: str, suits: list):
    for i in range(len(suits)):
        if suits[i]['name'] == suit:
            return i
    else:
        raise ValueError('Such suit does not exist')

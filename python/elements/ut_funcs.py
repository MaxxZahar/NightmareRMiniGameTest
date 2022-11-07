# Функции преобразования координат.
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

# Проверяем заполнен ли столбец полностью нужными фишками.


def check_full_column(column_number: int, map, suit: str):
    column = [el for i, el in enumerate(
        map.map) if i % map.number_of_columns == column_number]
    for el in column:
        if not el:
            return False
        if el.suit != suit:
            return False
    return True


# Отрисовываем экран победы.
def winner_screen(screen, img, font, number_of_moves):
    screen.blit(img, (0, 0))
    text = font.render("YOU WIN!", True, (0, 255, 0))
    text_2 = font.render(f'{number_of_moves} ходов', True, (0, 255, 0))
    textrect = text.get_rect()
    textrect.center = ((300, 250))
    textrect_2 = text_2.get_rect()
    textrect_2.center = ((300, 350))
    screen.blit(text, textrect)
    screen.blit(text_2, textrect_2)

import pygame
from pygame.locals import *
from field import Field, FieldMap
from suits import suits
from ut_funcs import d1tod2, get_suit_index, check_full_column, winner_screen


pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")
cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
pygame.mouse.set_cursor(cursor)

# Пути к нашим изображениям
bg_img = pygame.image.load('img/white_bg.png')
winner_bg_img = pygame.image.load('img/winner_bg.png')
block_img = pygame.image.load('img/block_sq.png')

# Отступы от границ экрана и между блоками
square_size = 50
margin_left = 100
margin_top = 100
margin_between = 100
margin_between_squares = 10

font = pygame.font.SysFont('georgia', 50, italic=True, bold=True)


# Класс элемента фишки на экране
class TokenSquare:
    def __init__(self, x, y, img, possible_directions, i, map):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.checked = False
        self.possible_directions = possible_directions
        self.index = i
        self.map = map

    # Грубо обновляем возможные направления движения. Применяется после обновления карты.
    def update_positions(self):
        self.possible_directions = []
        if self.index - self.map.number_of_columns >= 0 and not self.map.map[self.index - self.map.number_of_columns]:
            self.possible_directions.append('up')
        if self.index + self.map.number_of_columns < len(self.map) and not self.map.map[self.index + self.map.number_of_columns]:
            self.possible_directions.append('down')
        if self.index % self.map.number_of_columns and not self.map.map[self.index - 1]:
            self.possible_directions.append('left')
        if self.index % self.map.number_of_columns != self.map.number_of_columns - 1 and not self.map.map[self.index + 1]:
            self.possible_directions.append('right')


# Класс нашей игры.
class Game:
    def __init__(self, field: Field):
        self.columns_locations = field.settings['token_columns']
        self.map = field.map
        self.squares_list = []
        self.bar = []
        self.blocks = []
        self.number_of_moves = 0

        # Организуем список для полоски с индикаторами, показывающими, какие фишки собирать в данный столбец
        for i in range(field.settings['dimension'][1]):
            if i in self.columns_locations:
                j = self.columns_locations.index(i)
                img = pygame.transform.scale(
                    pygame.image.load(suits[j]['img']), (square_size, square_size))
                img_rect = img.get_rect()
                img_rect.x = margin_left + i * \
                    (square_size + margin_between_squares)
                img_rect.y = margin_top
                square = (img, img_rect)
                self.bar.append(square)

        for i, s in enumerate(self.map):
            if s:
                # Список для элементов блоков на поле.
                if s.entity == 'block':
                    img = pygame.transform.scale(
                        block_img, (square_size, square_size))
                    img_rect = img.get_rect()
                    coordinates = d1tod2(i, self.map.number_of_columns)
                    img_rect.x = margin_left + \
                        coordinates[0] * (square_size + margin_between_squares)
                    img_rect.y = margin_top + margin_between + \
                        coordinates[1] * (square_size +
                                          margin_between_squares) + square_size
                    square = (img, img_rect)
                    self.blocks.append(square)
                # Список для элементов фишек на поле.
                elif s.entity == 'token':
                    img_pre = pygame.image.load(
                        suits[get_suit_index(s.suit, suits)]['img'])
                    img = pygame.transform.scale(
                        img_pre, (square_size, square_size))
                    coordinates = d1tod2(i, self.map.number_of_columns)
                    x = margin_left + \
                        coordinates[0] * (square_size + margin_between_squares)
                    y = margin_top + margin_between + \
                        coordinates[1] * (square_size +
                                          margin_between_squares) + square_size
                    possible_directions = []
                    if i - self.map.number_of_columns >= 0 and not self.map.map[i - self.map.number_of_columns]:
                        possible_directions.append('up')
                    if i + self.map.number_of_columns < len(self.map) and not self.map.map[i + self.map.number_of_columns]:
                        possible_directions.append('down')
                    if i % self.map.number_of_columns and not self.map.map[i - 1]:
                        possible_directions.append('left')
                    if i % self.map.number_of_columns != self.map.number_of_columns - 1 and not self.map.map[i + 1]:
                        possible_directions.append('right')
                    square = TokenSquare(
                        x, y, img, possible_directions, i, self.map)
                    self.squares_list.append(square)
                else:
                    raise ValueError('Something wrong with the map')

    def draw_bar(self):
        for square in self.bar:
            screen.blit(square[0], square[1])

    def draw_blocks(self):
        for square in self.blocks:
            screen.blit(square[0], square[1])

    def draw_field(self):
        for square in self.squares_list:
            screen.blit(square.image, square.rect)

    def check_winning_condition(self):
        for i, column_number in enumerate(self.columns_locations):
            if not check_full_column(column_number, self.map, suits[i]['name']):
                return False
        return True


field = Field.create_field()
game = Game(field)

run = True
while run:

    # Отрисовываем элементы
    screen.blit(bg_img, (0, 0))
    game.draw_bar()
    game.draw_blocks()
    game.draw_field()
    # Проверяем условие победы.
    if game.check_winning_condition():
        winner_screen(screen, winner_bg_img, font, game.number_of_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Выбираем фишку для передвижения.
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for square in game.squares_list:
                if square.rect.collidepoint(pos) and not square.checked:
                    square.checked = True
                elif not square.rect.collidepoint(pos) and square.checked:
                    square.checked = False
        # Двигаем фишку, если можем и соответственно обновляем карту.
        elif event.type == pygame.KEYUP and [square for square in game.squares_list if square.checked]:
            checked_square = [
                square for square in game.squares_list if square.checked][0]
            if event.key == pygame.K_LEFT and 'left' in checked_square.possible_directions:
                checked_square.index -= 1
                checked_square.rect.x -= (square_size + margin_between_squares)
                game.map.map[checked_square.index] = game.map.map[checked_square.index + 1]
                game.map.map[checked_square.index + 1] = 0
                for square in game.squares_list:
                    square.update_positions()
                game.number_of_moves += 1
            if event.key == pygame.K_RIGHT and 'right' in checked_square.possible_directions:
                checked_square.index += 1
                checked_square.rect.x += (square_size + margin_between_squares)
                game.map.map[checked_square.index] = game.map.map[checked_square.index - 1]
                game.map.map[checked_square.index - 1] = 0
                for square in game.squares_list:
                    square.update_positions()
                game.number_of_moves += 1
            if event.key == pygame.K_UP and 'up' in checked_square.possible_directions:
                checked_square.index -= game.map.number_of_columns
                checked_square.rect.y -= (square_size + margin_between_squares)
                game.map.map[checked_square.index] = game.map.map[checked_square.index +
                                                                  game.map.number_of_columns]
                game.map.map[checked_square.index +
                             game.map.number_of_columns] = 0
                for square in game.squares_list:
                    square.update_positions()
                game.number_of_moves += 1
            if event.key == pygame.K_DOWN and 'down' in checked_square.possible_directions:
                checked_square.index += game.map.number_of_columns
                checked_square.rect.y += (square_size + margin_between_squares)
                game.map.map[checked_square.index] = game.map.map[checked_square.index -
                                                                  game.map.number_of_columns]
                game.map.map[checked_square.index -
                             game.map.number_of_columns] = 0
                for square in game.squares_list:
                    square.update_positions()
                game.number_of_moves += 1
    pygame.display.update()

pygame.quit()

import pygame
from pygame.locals import *
from field import Field, FieldMap
from suits import suits
from ut_funcs import d1tod2, get_suit_index


pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test")

bg_img = pygame.image.load('img/white_bg.png')
block_img = pygame.image.load('img/block_sq.png')

square_size = 50
margin_left = 100
margin_top = 100
margin_between = 100
margin_between_squares = 10


class Game:
    def __init__(self, field: Field):
        self.columns_locations = field.settings['token_columns']
        self.map = field.map
        self.squares_list = []
        self.bar = []

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
                    self.squares_list.append(square)
                elif s.entity == 'token':
                    img_pre = pygame.image.load(
                        suits[get_suit_index(s.suit, suits)]['img'])
                    img = pygame.transform.scale(
                        img_pre, (square_size, square_size))
                    img_rect = img.get_rect()
                    coordinates = d1tod2(i, self.map.number_of_columns)
                    img_rect.x = margin_left + \
                        coordinates[0] * (square_size + margin_between_squares)
                    img_rect.y = margin_top + margin_between + \
                        coordinates[1] * (square_size +
                                          margin_between_squares) + square_size
                    square = (img, img_rect)
                    self.squares_list.append(square)
                else:
                    raise ValueError('Something wrong with the map')

    def draw_bar(self):
        for square in self.bar:
            screen.blit(square[0], square[1])

    def draw_field(self):
        for square in self.squares_list:
            screen.blit(square[0], square[1])


field = Field.create_field()
game = Game(field)

run = True
while run:

    screen.blit(bg_img, (0, 0))
    game.draw_bar()
    game.draw_field()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

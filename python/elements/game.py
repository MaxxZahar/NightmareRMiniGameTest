import pygame
from pygame.locals import *
from field import Field, FieldMap
from settings import settings
from suits import suits


pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test")

bg_img = pygame.image.load('img/white_bg.png')

square_size = 50
margin_left = 100
margin_top = 100


class Game:
    def __init__(self, field: Field, settings: list):
        self.columns_locations = settings['token_columns']
        self.field = field
        self.squares_list = []
        self.bar = []

        # green_img = pygame.image.load('img/green_sq.png')
        # yellow_img = pygame.image.load('img/yellow_sq.png')
        # purple_img = pygame.image.load('img/purple_sq.png')
        # block_img = pygame.image.load('img/block_sq.png')

        for i in range(settings['dimension'][1]):
            if i in self.columns_locations:
                j = self.columns_locations.index(i)
                img = pygame.transform.scale(
                    pygame.image.load(suits[j]['img']), (square_size, square_size))
                img_rect = img.get_rect()
                img_rect.x = margin_left + i * square_size
                img_rect.y = margin_top
                square = (img, img_rect)
                self.bar.append(square)

    def draw_bar(self):
        for square in self.bar:
            screen.blit(square[0], square[1])


field = Field.create_field()
game = Game(field, settings)

run = True
while run:

    screen.blit(bg_img, (0, 0))
    game.draw_bar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

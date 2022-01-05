import random

import pygame
import os
import sys
from random import randrange

# Создание поля
pygame.init()
pygame.display.set_caption('Arcanoid')
size = width, height = 570, 400
screen = pygame.display.set_mode(size)
fps = 60

# переменная для предотвращения многократного отскока
st_y1 = 0


def load_image(name):  # load image
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# создание подвижной платформы-doska и шарика

doska_w = 100
doska_h = 20
doska_speed = 10
doska = pygame.Rect(250, 360, doska_w, doska_h)

ball_radius = 10
ball_speed = 3
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(290, 335, ball_rect, ball_rect)

# направления движения шарика по осям x,y
dx = 1
dy = -1
# создание блоков
blocks = [pygame.Rect(10 + 70 * i, 10 + 50 * j, 60, 40) for i in range(8) for j in range(5)]
colors = [(randrange(30, 255), randrange(30, 255), randrange(30, 255)) for i in range(8) for j in range(5)]


def ball_update():
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy


def collide():
    # отскок шарика от стенок
    global dx, dy, st_y1

    if ball.x >= 554 or ball.x <= 8:
        dx = -dx

    if ball.y < 5 or ball.y >= 378:
        dy = -dy

    # отскок шарика от платформы
    if ball.y <= st_y1 or st_y1 == 0:
        st_y1 = -1

    if pygame.Rect.colliderect(ball, doska) and st_y1 == -1:
        dy = -dy
        a = random.randint(0, 1)

        if a and ball.x > 7:
            dx = -dx

        st_y1 = ball.y - 50

    # отскок от плиток
    for block in blocks:
        if pygame.Rect.colliderect(block, ball):
            dy = -dy


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()
    # игровой цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('black')

        # создание объектов
        [pygame.draw.rect(screen, colors[color], block) for color, block in enumerate(blocks)]
        pygame.draw.rect(screen, 'blue', doska)
        pygame.draw.circle(screen, 'white', ball.center, ball_radius)

        # движение шарика
        ball_update()

        # отскок шарика
        collide()

        # управление
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and doska.left > 0:
            doska.left -= doska_speed
        if key[pygame.K_RIGHT] and doska.right < 570:
            doska.right += doska_speed

        # обновление экрана
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

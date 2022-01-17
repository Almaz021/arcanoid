import random

import pygame
import os
import sys
from random import randrange

# Создание поля
pygame.init()
pygame.display.set_caption('Arcanoid')
size = width, height = 570, 600
screen = pygame.display.set_mode(size)
fps = 60

# музыка
pygame.mixer.music.load("music/soundforgame.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
stopmusic = True

kick = pygame.mixer.Sound("music/kick.mp3")

# графика для анимации конца игры
all_sprites = pygame.sprite.Group()
im_x = -600
v = 200


def load_image(name):  # load image
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bit(pygame.sprite.Sprite):
    imager = load_image("gameover.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Bit.imager
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.rect.y = 150

    def update(self):
        self.rect.x = im_x


# переменная для предотвращения многократного отскока
st_y1 = 0

# создание подвижной платформы-doska и шарика

doska_w = 100
doska_h = 20
doska_speed = 10
doska = pygame.Rect(250, 570, doska_w, doska_h)

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

    if ball.y < 5:
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


def block_collid(dx, dy, ball, rect):
    # отскок от плиток
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def terminate():
    pygame.quit()
    sys.exit()


# Стартовое окно
def start_screen():
    clock1 = pygame.time.Clock()
    intro_text = ["ARKANOID", "Начать игру", "Выход"]
    font = pygame.font.Font(None, 60)
    string_rendered = font.render(intro_text[0], True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 160
    intro_rect.x = 170
    screen.blit(string_rendered, intro_rect)

    # кнопка начала игры
    font = pygame.font.Font(None, 40)
    button = font.render(intro_text[1], True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 280
    intro_rect.x = 200
    screen.blit(button, intro_rect)
    btn = pygame.Rect(181, 276, 200, 35)

    # кнопка выхода
    button1 = font.render(intro_text[2], True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 350
    intro_rect.x = 235
    screen.blit(button1, intro_rect)
    btn1 = pygame.Rect(181, 346, 200, 35)

    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()
            elif event1.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event1.pos):
                    print(1)
                    return
                elif btn1.collidepoint(event1.pos):
                    terminate()
            pygame.draw.rect(screen, (255, 255, 255), btn, 1)
            pygame.draw.rect(screen, (255, 255, 255), btn1, 1)
        pygame.display.flip()
        clock1.tick(fps)


if __name__ == '__main__':
    print(pygame.font.get_fonts())
    start_screen()
    running = True
    finishing = False
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

        # отскок шарика от стенок и платформы
        collide()

        # отскок шарика от блоков
        hit_index = ball.collidelist(blocks)
        if hit_index != -1:
            hit_rect = blocks.pop(hit_index)
            hit_color = colors.pop(hit_index)
            dx, dy = block_collid(dx, dy, ball, hit_rect)
            kick.play()

            # эффект исчезновения блока
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(screen, hit_color, hit_rect)

        # управление
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and doska.left > 0:
            doska.left -= doska_speed

        if key[pygame.K_RIGHT] and doska.right < 570:
            doska.right += doska_speed


        # Остановка и продолжение музыки по кнопке "пробел"
        if key[pygame.K_SPACE]:
            stopmusic = not stopmusic
            if stopmusic:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        # проверка на проигрыш или выигрыш
        if ball.y > 570:
            finishing = True
            break
        if not blocks:
            finishing = True
            break

        # обновление экрана
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    # анимация конца игры
    Bit(all_sprites)

    # создание шрифта
    basicFont = pygame.font.SysFont('georgia', 48)
    if blocks:
        text = basicFont.render('Вы проиграли', True, 'white', None)
    else:
        text = basicFont.render('Вы выиграли', True, 'white', None)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery


    while finishing:
        screen.fill('black')
        all_sprites.draw(screen)
        d = clock.tick() * v / 1000
        im_x += d
        all_sprites.update()
        if im_x >= -15:
            finishing = False

        # обновление экрана
        pygame.display.flip()

    while running:
        screen.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    # выход
    pygame.quit()


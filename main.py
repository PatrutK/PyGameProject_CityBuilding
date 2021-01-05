import pygame
import os
import sys

all_sprites = pygame.sprite.Group()
kursor_group = pygame.sprite.Group()


def load_image(name, color_key=None):  # нужна для подгрузки картинки в игру
    fullname = os.path.join('data', name)
    try:  # Выявляем ошибку
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Картинку не удаётся загрузить', fullname)
        raise SystemExit(message)
    if color_key is not None:  # Прозрачность картинки, если Нан, то она уже прозрачна
        if color_key == -1:  # Если передано -1, то по верхнему левому углу удаляем фон
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)  # Ставим фоном передаваемое значение
    return image


class Board:  # отрисовка поля
    def __init__(self, screen):  # так удобнее
        self.width = 50
        self.height = 100
        self.board = [[0] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20
        self.screen = screen

    def render(self):
        color = pygame.Color(80, 80, 80)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.screen, color, (
                    self.left + y * self.cell_size, self.top + x * self.cell_size, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_position):
        self.cell_x = (mouse_position[0] - self.left) // self.cell_size
        self.cell_y = (mouse_position[1] - self.top) // self.cell_size
        if (0 <= self.cell_x < self.width) and (0 <= self.cell_y < self.height):
            print(self.cell_x, self.cell_y)
            return self.cell_x, self.cell_y

    def on_click(self, cell_coordinates):
        if cell_coordinates:
            self.board[self.cell_y][self.cell_x] = (self.board[self.cell_y][self.cell_x] + 1)


class Kursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('kursor.png', -1)
        self.rect = self.image.get_rect()  # Получаем размеры "Прямоугольника" спрайта
        self.rect = self.rect.move(200, 200)

        self.add(kursor_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -20)
        print(self.rect.x, self.rect.y)

    def move_down(self):
        self.rect = self.rect.move(0, +20)

    def move_left(self):
        self.rect = self.rect.move(-20, 0)

    def move_right(self):
        self.rect = self.rect.move(+20, 0)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        # print(target.rect.x, target.rect.w // 2)
        # print(WIDTH_SIZE)
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH_SIZE // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT_SIZE // 2)


class ResidentialBuildings():
    def __init__(self, *args):
        super().__init__()
        pass


class IndustrialBuildings():
    def __init__(self, *args):
        super().__init__()
        pass
        #  сельхоз, заводы


class CultureBuildings():
    def __init__(self, *args):
        super().__init__()
        pass
    #  кружки, театр, парки


class EntertainmentBuildings():
    def __init__(self, *args):
        super().__init__()
        pass
    #  площадки, кино


class Road():
    def __init__(self, *args):
        super(Road, self).__init__()
        pass
    #  дороги


def load_image(name, color_key=None):  # нужна для подгрузки картинки в игру
    fullname = os.path.join('data', name)
    try:  # Выявляем ошибку
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Картинку не удаётся загрузить', fullname)
        raise SystemExit(message)
    if color_key is not None:  # Прозрачность картинки, если Нан, то она уже прозрачна
        if color_key == -1:  # Если передано -1, то по верхнему левому углу удаляем фон
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)  # Ставим фоном передаваемое значение
    return image


if __name__ == '__main__':
    pygame.init()
    WIDTH_SIZE, HEIGHT_SIZE = 800, 800
    FPS = 60

    screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE))
    pygame.display.set_caption('Панельки')

    fon_image = load_image('map.png')
    fonWidth, fonHeight = fon_image.get_rect().size

    main = Board(screen)
    kursor = Kursor()
    camera = Camera()
    clock = pygame.time.Clock()

    running = True
    main_build = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    kursor.move_up()
                    # print(kursor.rect.x, kursor.rect.y, kursor.rect.w, kursor.rect.h)
                elif event.key == pygame.K_DOWN:
                    kursor.move_down()
                elif event.key == pygame.K_RIGHT:
                    kursor.move_right()
                elif event.key == pygame.K_LEFT:
                    kursor.move_left()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Выход из игры
            running = False

        if keys[pygame.K_SPACE]:  # Режим редактирования карты
            main_build = not main_build
            if main_build:
                pass

        screen.blit(fon_image, (0, 0))
        main.render()
        all_sprites.draw(screen)
        camera.update(kursor)
        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()

    pygame.quit()

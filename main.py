import pygame
import sys
import os
import pygame_gui


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


def terminate():
    pygame.quit()
    sys.exit()


def load_level(name):
    fullname = "data/" + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map


def draw_level(level_map):
    new_player, x, y = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('grass.png', x, y)  # Спрайт травы
            elif level_map[y][x] == '#':
                Tile('water.png', x, y)  # Спрайт воды
            elif level_map[y][x] == '@':  # Спрайт персонажа + под него спрайт травы
                Tile('grass.png', x, y)
                new_player = Kursor(x, y)
            elif level_map[y][x] == '>':  # Спрайт песка (вода справа)
                Tile('sand1.png', x, y)
            elif level_map[y][x] == '<':  # Спрайт песка (вода слева)
                Tile('sand2.png', x, y)
            elif level_map[y][x] == '&':  # Спрайт леса (ограничитель карты)
                Tile('Forest.png', x, y)
            elif level_map[y][x] == '!':  # Спрайт песка (вода снизу)
                Tile('sand.png', x, y)
            elif level_map[y][x] == '^':  # Спрайт песка (вода сверху)
                Tile('sand3.png', x, y)
            elif level_map[y][x] == '1':  # Спрайт песка (угловой, вода справа-снизу)
                Tile('sand4.png', x, y)
            elif level_map[y][x] == '2':  # Спрайт песка (угловой, вода слева-снизу)
                Tile('sand7.png', x, y)
            elif level_map[y][x] == '3':  # Спрайт песка (угловой, вода справа-сверху)
                Tile('sand5.png', x, y)
            elif level_map[y][x] == '4':  # Спрайт песка (угловой, вода слева-снизу)
                Tile('sand6.png', x, y)
    return new_player, x, y


def print_text(message, x, y, font_color=(255, 0, 0), font_type='shrift.ttf', font_size=30):  # вывод текста на экран
    font_type1 = pygame.font.Font(font_type, font_size)
    text = font_type1.render(message, True, font_color)
    screen.blit(text, (x, y))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image(tile_type)
        self.rect = self.image.get_rect().move(25 * pos_x, 25 * pos_y)

        if tile_type == 'water.png' or tile_type == 'forest.png':
            self.add(box_group, tiles_group, all_sprites)
        else:
            self.add(tiles_group, all_sprites)


class Kursor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('kursor.png', -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(1 * pos_x, 1 * pos_y)

        self.add(player_group, all_sprites)

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, +50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        self.rect = self.rect.move(+50, 0)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
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


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

kursor, level_x, level_y = draw_level(load_level("map.txt"))

if __name__ == '__main__':
    pygame.init()
    WIDTH_SIZE, HEIGHT_SIZE = 1000, 900
    screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE))

    clock = pygame.time.Clock()
    fps = 60

    camera = Camera()

    manager = pygame_gui.UIManager((WIDTH_SIZE, HEIGHT_SIZE))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 150), (10, 10)),  # Размеры и расположение кнопки
        text='hello world',  # Текст на кнопке
        manager=manager  # Менеджер кнопки
    )

    running = True
    main_build = True

    while running:
        time_delta = clock.tick(fps) / 1000.0  # некоторые элементы ПИ имеют таймер, поэтому нужна эта переменная
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                kursor.move_up()
                # if pygame.sprite.spritecollideany(kursor, box_group):
                #     kursor.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                kursor.move_down()
                # if pygame.sprite.spritecollideany(player, box_group):
                #     player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                kursor.move_left()
                # if pygame.sprite.spritecollideany(player, box_group):
                #     player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                kursor.move_right()
                # if pygame.sprite.spritecollideany(player, box_group):
                #     player.move_left()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:  #
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  #
                    if event.ui_element == button:
                        print('d')

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Выход из игры
            terminate()

        if keys[pygame.K_SPACE]:  # Режим редактирования карты
            main_build = not main_build
            if main_build:
                pass
                # print_text('Режим строительства', 10, 10)

        camera.update(kursor)
        for sprite in all_sprites:
            camera.apply(sprite)

        # fon_image = load_image('map1.png')
        # screen.blit(fon_image, (0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)

    terminate()

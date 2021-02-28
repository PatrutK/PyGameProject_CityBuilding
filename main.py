import pygame
import os
import pygame_gui
import sys
from random import *

all_sprites = pygame.sprite.Group()


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


def show_menu():
    global running

    menu_back = pygame.image.load('data/menu_back.png')
    menu_run = True
    start_screen = pygame.display.set_mode((1420, 920))
    start_clock = pygame.time.Clock()

    start_manager = pygame_gui.UIManager(
        (1420, 920))  # Обрабатывает функции обновления ПИ, которые мы создаём и передаем ему

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((460, 300), (500, 100)),  # размеры и положение
        text='Начать',  # текст
        manager=start_manager  # указываем на наш менеджер
    )

    end_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((460, 450), (500, 100)),  # размеры и положение
        text='Выйти из игры',  # текст
        manager=start_manager  # указываем на наш менеджер
    )

    while menu_run:
        time_dl = start_clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # указываем на событие нажатие кнопки
                    if event.ui_element == start_btn:
                        menu_run = False
                    if event.ui_element == end_btn:
                        menu_run = False
                        running = False
            start_manager.process_events(event)

        start_manager.update(time_dl)
        start_screen.blit(menu_back, (0, 0))
        start_manager.draw_ui(start_screen)
        pygame.display.update()


class Board:  # отрисовка поля
    def __init__(self, screen):
        self.height = 70
        self.width = 70
        self.board = [[0] * self.width for _ in range(self.height)]
        self.left = 10
        self.top = 60
        self.cell_size = 20
        self.screen = screen

        start_int = IndustrialBuildings(190, 160)
        start_res = ResidentialBuildings (210, 240)

    def render(self):
        color = pygame.Color(80, 80, 80)
        for y in range(self.width):
            for x in range(self.height):
                pygame.draw.rect(self.screen, color, (
                    self.left + y * self.cell_size, self.top + x * self.cell_size, self.cell_size,
                    self.cell_size), 1)
        self.board[1][8] = -1
        self.board[1][9] = -1
        self.board[1][10] = -1
        self.board[3][8] = -1
        self.board[3][9] = -1
        self.board[3][10] = -1
        self.board[0][9] = -1
        self.board[0][10] = -1

    def get_cell(self, mouse_position):
        self.cell_x = (mouse_position[0] - self.left) // self.cell_size
        self.cell_y = (mouse_position[1] - self.top) // self.cell_size
        if (0 <= self.cell_x < self.height) and (0 <= self.cell_y < self.width):
            print(self.board[self.cell_y][self.cell_x])
            return self.cell_x, self.cell_y
        else:
            return None

    # def on_click(self):
    #     print(self.board[self.cell_y][self.cell_x])

    def build(self, mouse_pos):
        global ind_count
        cell = self.get_cell(mouse_pos)
        if self.board[self.cell_y][self.cell_x] == -1 or cell is None:
            pass
        else:
            if current_build == 'Жилое здание':
                if self.board[self.cell_y - 1][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x + 3] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x + 3] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x] == -1 or \
                        self.board[self.cell_y][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y][self.cell_x + 3] == -1 or money_count <= 50:
                    print('error')
                else:
                    res_build = ResidentialBuildings(mouse_pos[0] // 20 * self.cell_size + self.left,
                                                     mouse_pos[1] // 20 * self.cell_size)
                    res_build.new_stat()
                    update_all_stats()
                    self.board[self.cell_y + 1][self.cell_x], \
                    self.board[self.cell_y + 1][self.cell_x + 1], \
                    self.board[self.cell_y + 1][self.cell_x + 2], \
                    self.board[self.cell_y][self.cell_x], \
                    self.board[self.cell_y][self.cell_x + 1], \
                    self.board[self.cell_y][self.cell_x + 2] = -1, -1, -1, -1, -1, -1
            elif current_build == 'Производство':
                if self.board[self.cell_y - 1][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x + 4] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x + 4] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x] == -1 or \
                        self.board[self.cell_y][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y][self.cell_x + 4] == -1 or money_count <= 75:
                    print('error')
                else:
                    ind_build = IndustrialBuildings(mouse_pos[0] // 20 * self.cell_size + self.left,
                                                    mouse_pos[1] // 20 * self.cell_size)
                    ind_build.new_stat()
                    update_all_stats()
                    ind_count += 1
                    self.board[self.cell_y + 1][self.cell_x], \
                    self.board[self.cell_y + 1][self.cell_x + 1], \
                    self.board[self.cell_y + 1][self.cell_x + 2], \
                    self.board[self.cell_y + 1][self.cell_x + 3], \
                    self.board[self.cell_y + 2][self.cell_x], \
                    self.board[self.cell_y + 2][self.cell_x + 1], \
                    self.board[self.cell_y + 2][self.cell_x + 2], \
                    self.board[self.cell_y + 2][self.cell_x + 3], \
                    self.board[self.cell_y][self.cell_x], \
                    self.board[self.cell_y][self.cell_x + 1], \
                    self.board[self.cell_y][self.cell_x + 2], \
                    self.board[self.cell_y][self.cell_x + 3] = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
            elif current_build == 'Здание культуры':
                if self.board[self.cell_y - 1][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x + 3] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x + 3] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x] == -1 or \
                        self.board[self.cell_y + 3][self.cell_x] == -1 or \
                        self.board[self.cell_y][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y][self.cell_x + 3] == -1:
                    print('error')
                else:
                    cult_build = CultureBuildings(mouse_pos[0] // 20 * self.cell_size + self.left,
                                                  mouse_pos[1] // 20 * self.cell_size)
                    cult_build.new_stat()
                    update_all_stats()
                    self.board[self.cell_y + 1][self.cell_x], \
                    self.board[self.cell_y + 1][self.cell_x + 1], \
                    self.board[self.cell_y + 1][self.cell_x + 2], \
                    self.board[self.cell_y + 2][self.cell_x], \
                    self.board[self.cell_y + 2][self.cell_x + 1], \
                    self.board[self.cell_y + 2][self.cell_x + 2], \
                    self.board[self.cell_y][self.cell_x], \
                    self.board[self.cell_y][self.cell_x + 1], \
                    self.board[self.cell_y][self.cell_x + 2] = -1, -1, -1, -1, -1, -1, -1, -1, -1
            elif current_build == 'Развлечение':
                if self.board[self.cell_y - 1][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x + 4] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x + 4] == -1 or \
                        self.board[self.cell_y - 1][self.cell_x] == -1 or \
                        self.board[self.cell_y + 2][self.cell_x] == -1 or \
                        self.board[self.cell_y][self.cell_x - 1] == -1 or \
                        self.board[self.cell_y][self.cell_x + 4] == -1:
                    print('error')
                else:
                    ent_build = EntertainmentBuildings(mouse_pos[0] // 20 * self.cell_size + self.left,
                                                       mouse_pos[1] // 20 * self.cell_size)
                    ent_build.new_stat()
                    update_all_stats()
                    self.board[self.cell_y + 1][self.cell_x], \
                    self.board[self.cell_y + 1][self.cell_x + 1], \
                    self.board[self.cell_y + 1][self.cell_x + 2], \
                    self.board[self.cell_y + 1][self.cell_x + 3], \
                    self.board[self.cell_y][self.cell_x], \
                    self.board[self.cell_y][self.cell_x + 1], \
                    self.board[self.cell_y][self.cell_x + 2], \
                    self.board[self.cell_y][self.cell_x + 3] = -1, -1, -1, -1, -1, -1, -1, -1

def update_all_stats():
    global workplace, happines_count, humans_count, soiling

    if humans_count > workplace or soiling > 60:
        if happines_count > 0:
            happines_count -= 15
        return happines_count


class ResidentialBuildings(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = load_image("build1.png")
        self.rect = self.image.get_rect().move(x, y)

    def new_stat(self):
        global money_count, humans_count
        money_count -= 50
        humans_count += 50
        return money_count, humans_count


class IndustrialBuildings(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = load_image("zavod_build.png")
        self.rect = self.image.get_rect().move(x, y)

    def new_stat(self):
        global money_count, workplace, happines_count, soiling
        money_count -= 75
        workplace += 75
        happines_count -= 10
        if happines_count > 0 and happines_count < 100:
            happines_count -= 5
        elif soiling > 0 and soiling < 100:
            soiling += 20
        return money_count, workplace, happines_count, soiling


class CultureBuildings(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = load_image("dk_build.png")
        self.rect = self.image.get_rect().move(x, y)

    def new_stat(self):
        global money_count, happines_count, soiling
        money_count -= 35
        if happines_count > 0 and happines_count < 100:
            happines_count += 10
        elif soiling < 100 and soiling > 0:
            soiling -= 10
        return money_count, happines_count, soiling


class EntertainmentBuildings(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = load_image("kino_build.png")
        self.rect = self.image.get_rect().move(x, y)

    def new_stat(self):
        global money_count, happines_count
        money_count -= 75
        if happines_count > 0 and happines_count < 100:
            happines_count += 15
        return money_count, happines_count


# class Road():
#     def __init__(self, *args):
#         pass
#     #  дороги


if __name__ == '__main__':
    pygame.init()
    WIDTH_SIZE, HEIGHT_SIZE = 1420, 920
    FPS = 60
    color = 'black'

    screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE))
    pygame.display.set_caption('Панельки')

    board = Board(screen)
    clock = pygame.time.Clock()

    running = True
    main_build = False
    current_build = None

    money_count = 300
    humans_count = 50
    happines_count = 50
    days_count = 1
    month_numb = 6
    soiling = 20
    workplace = 75
    ind_count = 1

    month = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
             9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

    manager = pygame_gui.UIManager(
        (WIDTH_SIZE, HEIGHT_SIZE))  # Обрабатывает функции обновления ПИ, которые мы создаём и передаем ему

    switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (120, 40)),  # размеры и положение
        text='Режим стройки',  # текст
        manager=manager  # указываем на наш менеджер
    )

    buildungs_drop_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Жилое здание', 'Производство', 'Здание культуры', 'Развлечение'],
        starting_option='Список зданий',
        relative_rect=pygame.Rect((140, 10), (160, 40)),  # размеры и положение
        manager=manager
    )

    next_day_bttn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((1282, 10), (130, 42)),  # размеры и положение
        text='Слeдующий день',  # текст
        manager=manager  # указываем на наш менеджер
    )

    buildungs_drop_menu.hide()
    show_menu()

    while running:
        time_delta = clock.tick(FPS) / 1000.0  # некоторые события ПИ используют таймеры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((200, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',  # название окна
                    action_long_desc='Вы уверены, что хотите выйти?',  # содержимое окошка
                    action_short_name='OK',  # Название кнопки подтверждения
                    blocking=True  # Игнорирует любое нажатие, пока мы не нажмем на кнопку
                )

            if event.type == pygame.USEREVENT:  # указываем на пользоваетльское событие
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False

                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    current_build = event.text

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # указываем на событие нажатие кнопки
                    if event.ui_element == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        current_build = event.text
                    if event.ui_element == switch:
                        if color == 'black':
                            color = 'gray'
                            buildungs_drop_menu.show()
                            main_build = True
                        else:
                            color = 'black'
                            buildungs_drop_menu.hide()
                            main_build = False
                        screen.fill(pygame.Color(color))

                    if event.ui_element == next_day_bttn:
                        humans_count += randint(5, 20)
                        if workplace < humans_count:
                            money_count += 10 * ind_count
                        else:
                            money_count += 30 * ind_count
                        days_count += 1
                        soiling += 5 * ind_count
                        update_all_stats()
                        if month_numb == 12 and days_count == 32:
                            month_numb = 1
                            days_count = 1
                        elif month_numb % 2 != 0 and days_count == 32:
                            month_numb += 1
                            days_count = 1
                        elif month_numb == 2 and days_count == 29:
                            month_numb += 1
                            days_count = 1
                        elif month_numb % 2 == 0 and days_count == 31 and month[month_numb] != 'Декабрь':
                            month_numb += 1
                            days_count = 1

            if main_build == True and not (current_build == None):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.build(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_cell(event.pos)

            manager.process_events(event)
        manager.update(time_delta)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Выход из игры
            running = False

        work_place_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Раб.места: {workplace}',
            relative_rect=pygame.Rect((325, 10), (115, 40)),
            manager=manager
        )

        money_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Бюджет: {money_count}',
            relative_rect=pygame.Rect((455, 10), (100, 40)),
            manager=manager
        )

        humans_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Население: {humans_count}',
            relative_rect=pygame.Rect((570, 10), (130, 40)),
            manager=manager
        )

        soiling_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Загрязнение: {soiling}%',
            relative_rect=pygame.Rect((715, 10), (160, 40)),
            manager=manager
        )

        happines_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Уровень счастья: {happines_count}%',
            relative_rect=pygame.Rect((890, 10), (170, 40)),
            manager=manager
        )

        days_label = pygame_gui.elements.ui_label.UILabel(
            text=f'День: {days_count} Месяц: {month[month_numb]}',
            relative_rect=pygame.Rect((1075, 10), (195, 40)),
            manager=manager
        )

        if keys[pygame.K_1]:
            pass
        screen.fill(pygame.Color(color))

        board.render()
        all_sprites.draw(screen)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

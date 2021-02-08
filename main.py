import pygame
import os
import pygame_gui
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
        self.height = 42
        self.width = 70
        self.board = [[0] * self.height for _ in range(self.width)]
        self.left = 10
        self.top = 60
        self.cell_size = 20
        self.screen = screen

    def render(self):
        color = pygame.Color(80, 80, 80)
        for y in range(self.width):
            for x in range(self.height):
                pygame.draw.rect(self.screen, color, (
                    self.left + y * self.cell_size, self.top + x * self.cell_size, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_position):
        self.cell_x = (mouse_position[0] - self.left) // self.cell_size
        self.cell_y = (mouse_position[1] - self.top) // self.cell_size
        if (0 <= self.cell_x < self.height) and (0 <= self.cell_y < self.width):
            print(self.cell_x, self.cell_y)
            return self.cell_x, self.cell_y

    def on_click(self, cell_coordinates):
        if cell_coordinates:
            self.board[self.cell_y][self.cell_x] = (self.board[self.cell_y][self.cell_x] + 1)


# class ResidentialBuildings():
#     def __init__(self, *args):
#         pass
#
#
# class IndustrialBuildings():
#     def __init__(self, *args):
#         pass
#         #  сельхоз, заводы
#
#
# class CultureBuildings():
#     def __init__(self, *args):
#         pass
#     #  кружки, театр, парки
#
#
# class EntertainmentBuildings():
#     def __init__(self, *args):
#         pass
#     #  площадки, кино
#
#
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
    main_build = True

    money_count = 0
    humans_count = 0
    happines_count = 0

    manager = pygame_gui.UIManager(
        (WIDTH_SIZE, HEIGHT_SIZE))  # Обрабатывает функции обновления ПИ, которые мы создаём и передаем ему

    switch = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (120, 40)),  # размеры и положение
        text='Режим стройки',  # текст
        manager=manager  # указываем на наш менеджер
    )

    buildungs_drop_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Easy', 'Medium', 'Hard'],
        starting_option='Easy',
        relative_rect=pygame.Rect((140, 10), (100, 40)),  # размеры и положение
        manager=manager
    )

    buildungs_drop_menu.hide()

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
                    print('работает', event.text)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # указываем на событие нажатие кнопки
                    if event.ui_element == switch:
                        if color == 'black':
                            color = 'gray'
                            buildungs_drop_menu.show()
                        else:
                            color = 'black'
                            buildungs_drop_menu.hide()
                        screen.fill(pygame.Color(color))

            manager.process_events(event)
        manager.update(time_delta)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Выход из игры
            running = False

        if keys[pygame.K_SPACE]:  # Режим редактирования карты
            main_build = not main_build
            if main_build:
                pass

        money_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Бюджет: {money_count}',
            relative_rect=pygame.Rect((540, 10), (100, 40)),
            manager=manager
        )

        humans_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Население: {humans_count}',
            relative_rect=pygame.Rect((650, 10), (120, 40)),
            manager=manager
        )

        happines_label = pygame_gui.elements.ui_label.UILabel(
            text=f'Уровень счастья: {happines_count}',
            relative_rect=pygame.Rect((780, 10), (160, 40)),
            manager=manager
        )

        if keys[pygame.K_1]:
            money_count += 3
            humans_count += 5
            happines_count += 1

        screen.fill(pygame.Color(color))
        all_sprites.draw(screen)

        board.render()
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

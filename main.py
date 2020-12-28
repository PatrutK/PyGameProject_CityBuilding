import pygame


class Board:  # отрисовка поля
    def __init__(self, width, height, left=10, top=10, cell_size=20):  # так удобнее
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color(80, 80, 80)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, color, (
                    self.left + y * self.cell_size, self.top + x * self.cell_size, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_position):
        self.cell_x = (mouse_position[0] - self.left) // self.cell_size
        self.cell_y = (mouse_position[1] - self.top) // self.cell_size
        if (0 <= self.cell_x < self.width) and (0 <= self.cell_y < self.height):
            return self.cell_x, self.cell_y

    def on_click(self, cell_coordinates):
        if cell_coordinates:
            self.board[self.cell_y][self.cell_x] = (self.board[self.cell_y][self.cell_x] + 1)


class ResidentialBuildings(Board):
    def __init__(self, *args, **k_args):
        super().__init__()
        pass


class IndustrialBuildings(Board):
    def __init__(self, *args):
        super().__init__()
        pass
        #  сельхоз, заводы


class CultureBuildings(Board):
    def __init__(self, *args):
        super().__init__()
        pass
    #  кружки, театр, парки


class EntertainmentBuildings(Board):
    def __init__(self, *args):
        super().__init__()
        pass
    #  площадки, кино


class Road(Board):
    def __init__(self, *args):
        super(Road, self).__init__()
        pass
    #  дороги


if __name__ == '__main__':
    pygame.init()
    size = 1920, 1000
    screen = pygame.display.set_mode(size)
    board = Board(49, 95)
    homes = ResidentialBuildings
    pygame.display.set_caption('Панельки')
    running = True
    main_build = True  # режим наблюдателя

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Выход из игры
            running = False

        if keys[pygame.K_LALT]:  # Сворачивание окна
            pygame.display.iconify()

        if keys[pygame.K_SPACE]:  # Режим редактирования карты
            main_build = not main_build
            if main_build:
                board.render(screen)
                pygame.display.flip()

    pygame.quit()

import sys
import time
import random
from PyQt5 import *  # QtCore, QtGui, QtWidgets
import pygame  # from pygame.locals import *


# class MainMenu(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("PROJECT.ui", self)


class Board:  # отрисовка поля
    def __init__(self, width, height, left=5, top=5, cell_size=20):  # так удобнее
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


class ResidentialBuildings:  # здесь будут происходить основные действия, вплане геймплея - случайные события, стастика, игровые дни и т.д.
    def __init__(self, *args, **k_args):
        super().__init__()
        pass

    def get_click(self, mouse_position):
        cell = self.get_cell(mouse_position)
        self.on_click(cell)
        pygame.draw.rect(screen, (255, 255, 255),
                         (event.pos[0], event.pos[1], self.cell_size * 4, self.cell_size * 3))


class IndustrialBuildings:
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
    size = 0, 1  # не нужная переменная, вернее нужная, но у нас же fullscreen!
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    board = Board(35, 63, 10, 10, 20)
    homes = ResidentialBuildings
    pygame.display.set_caption('Панельки')  # это не нужно, ибо у нас fullscreen (название не видно)
    running = True
    main_build = True  # режим наблюдателя
    build_1 = False
    build_2 = False
    build_3 = False
    build_4 = False
    build_5 = False
    build_6 = False

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
            # if not main_build:
            #     screen.fill((0, 0, 0))
            #     pygame.display.flip()
        if keys[pygame.K_1]:
            build_1 = True
            build_2, build_3, build_4, build_5, build_6 = False
        # ВЫБРАТЬ постройку - далее будем кликать мышкой на поле (поле, дом, завод, кино)
        if keys[pygame.K_2]:
            build_2 = True
            build_1, build_3, build_4, build_5, build_6 = False

        if keys[pygame.K_3]:
            build_3 = True
            build_1, build_2, build_4, build_5, build_6 = False

        if keys[pygame.K_4]:
            build_4 = True
            build_1, build_2, build_3, build_5, build_6 = False

        if keys[pygame.K_5]:
            build_5 = True
            build_1, build_2, build_3, build_4, build_6 = False

        if keys[pygame.K_6]:
            build_6 = True
            build_1, build_2, build_3, build_4, build_5 = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and build_1:  # Постройка зданий - завод
                homes.get_click()
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and build_2:  # Постройка зданий - дом
                board.get_click(event.pos)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and build_3:  # Постройка зданий - кинотеатр
                board.get_click(event.pos)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and build_4:  # Постройка зданий - поле (ферма)
                board.get_click(event.pos)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and build_5:  # Постройка зданий - банк
                board.get_click(event.pos)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN and build_6:  # Постройка зданий - музей
                board.get_click(event.pos)
                pygame.display.flip()
    pygame.quit()

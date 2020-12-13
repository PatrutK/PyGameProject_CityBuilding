import pygame


class Board:
    def __init__(self, width, height, left, top, cell_size):
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
                    self.left + y * self.cell_size, self.top + x * self.cell_size, self.cell_size, self.cell_size), 1)


if __name__ == '__main__':
    pygame.init()
    size = 2, 1000
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    board = Board(50, 95, 10, 10, 20)
    pygame.display.set_caption('Панельки')

    running = True
    build = False

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
            build = not build
            if build:
                board.render(screen)
                pygame.display.flip()
            # if not build:
            #     screen.fill((0, 0, 0))
            #     pygame.display.flip()

        if keys[pygame.K_1] and build:  # Постройка зданий
            pygame.draw.rect(screen, (255, 255, 255), (20, 20, 100, 50))
            pygame.display.flip()

    pygame.quit()

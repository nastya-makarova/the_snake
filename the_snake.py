from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет границ сетки
BORDER_GRID_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Заполнить фон окна черным цветом.
screen.fill(BOARD_BACKGROUND_COLOR)


def draw_lines():
    """Функция для отрисовки линий на игровом поле."""
    # Горизонтальные линии.
    for i in range(GRID_HEIGHT + 1):
        if i == GRID_HEIGHT:
            pygame.draw.line(
                screen, BORDER_GRID_COLOR,
                (0, i * GRID_SIZE - 1),
                (SCREEN_WIDTH, i * GRID_SIZE - 1), 1)
        else:
            pygame.draw.line(
                screen, BORDER_GRID_COLOR,
                (0, i * GRID_SIZE),
                (SCREEN_WIDTH, i * GRID_SIZE), 1)

    # Вертикальные линии.
    for i in range(GRID_WIDTH + 1):
        if i == GRID_WIDTH:
            pygame.draw.line(
                screen, BORDER_GRID_COLOR,
                (i * GRID_SIZE - 1, 0),
                (i * GRID_SIZE - 1, SCREEN_HEIGHT), 1)
        else:
            pygame.draw.line(
                screen, BORDER_GRID_COLOR,
                (i * GRID_SIZE, 0),
                (i * GRID_SIZE, SCREEN_HEIGHT), 1)


# Описание всех классов игры.
class GameObject:
    """Базовый класс"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Kласс, унаследованный от GameObject,"""

    """описывающий яблоко и действия с ним."""

    def randomize_position(self):
        """Метод устанавливает случайное положение яблока на игровом поле."""
        self.random_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.random_position

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def draw(self):
        """Метод отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color,
                         rect.move(1, 1).inflate(-1, -1))
        pygame.draw.rect(screen, BORDER_COLOR, rect.inflate(1, 1), 1)


class Snake(GameObject):
    """Kласс, унаследованный от GameObject,"""

    """описывающий змею и действия с ней."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод отрисовывает змею на игровой поверхности."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect.inflate(1, 1), 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect.inflate(1, 1), 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                             last_rect.move(1, 1).inflate(-1, -1))
            pygame.draw.rect(screen, BORDER_GRID_COLOR,
                             last_rect.inflate(1, 1), 1)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        head_position = self.positions[0]
        return head_position

    def move(self):
        """Метод обновляет позицию змейки."""
        head = self.get_head_position()

        if head[1] == 0 and self.direction == UP:
            list.insert(self.positions, 0,
                        (head[0], SCREEN_HEIGHT - GRID_SIZE))
        elif head[1] == SCREEN_HEIGHT - GRID_SIZE and self.direction == DOWN:
            list.insert(self.positions, 0, (head[0], 0))
        elif head[0] == 0 and self.direction == LEFT:
            list.insert(self.positions, 0, (SCREEN_WIDTH - GRID_SIZE, head[1]))
        elif head[0] == SCREEN_WIDTH - GRID_SIZE and self.direction == RIGHT:
            list.insert(self.positions, 0, (0, head[1]))
        else:
            list.insert(self.positions, 0,
                        ((head[0] + self.direction[0] * GRID_SIZE),
                         (head[1] + self.direction[1] * GRID_SIZE)))

        for position in self.positions[2:]:
            if head == position:
                self.reset()

        if self.length == len(self.positions):
            self.last = None
        else:
            self.last = list.pop(self.positions, -1)

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние"""
        """после столкновения с собой."""
        draw_lines()
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(DIRECTIONS)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def create_apple(snake):
    """Функция создания яблока с корректными координатами."""
    apple = Apple()
    while apple.position in snake.positions:
        apple = Apple()
    return apple


def main():
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    draw_lines()
    snake = Snake()
    apple = create_apple(snake)
    snake.draw()
    apple.draw()
    pygame.display.update()

    while True:

        clock.tick(SPEED)

        draw_lines()

        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = create_apple(snake)
            apple.draw()

        if snake.positions[0] in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple = create_apple(snake)
            apple.draw()

        snake.move()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()

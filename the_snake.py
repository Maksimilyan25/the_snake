from random import randint
import pygame as pg

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FONT_SIZE = 36
FONT = ('Arial', 16)
TEXT_COLOR = (255, 255, 255)

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отрисовка головы."""


class Apple(GameObject):
    """Класс для яблока, которое змейка должна съесть."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        if occupied_positions is not None:
            self.randomize_position(occupied_positions)
        else:
            pass

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение яблока на игровом поле,
        избегая занятых клеток.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки с учетом выхода за границы экрана."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head_x = head_x + dx * GRID_SIZE
        new_head_y = head_y + dy * GRID_SIZE

    # Обработка выхода за границы экрана
        new_head_x %= SCREEN_WIDTH
        new_head_y %= SCREEN_HEIGHT

        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_RETURN:
                return True  # Для рестарта игры
    return False


def draw_menu():
    """Отрисовывает меню начала игры."""
    font = pg.font.SysFont(FONT, FONT_SIZE)
    text = font.render('Нажмите Enter для старта', True, (TEXT_COLOR))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


def main():
    """Основной игровой цикл."""
    snake = Snake()
    game_started = False
    apple = None
    occupied_positions = set(snake.positions)
    if apple is None:
        apple = Apple(occupied_positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        if not game_started:
            draw_menu()
            if handle_keys(snake):
                game_started = True
                snake.reset()  # Сброс змейки
        elif snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions)
        else:
            handle_keys(snake)
            snake.update_direction()
            snake.move()
            # Проверка столкновения с самим собой
            if snake.positions[0] in snake.positions[1:]:
                game_started = False  # Включаем меню
                snake.reset()  # Сброс змейки

            apple.draw()
            snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()

import pygame
import random

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 360
GRID_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Maze of Terms")

# Загрузка изображений
wall_img = pygame.transform.scale(pygame.image.load("assets/wall.png"), (GRID_SIZE, GRID_SIZE))
earth_img = pygame.transform.scale(pygame.image.load("assets/earth.png"), (GRID_SIZE, GRID_SIZE))
player_img = pygame.transform.scale(pygame.image.load("assets/boy.png"), (GRID_SIZE, GRID_SIZE))
key_img = pygame.transform.scale(pygame.image.load("assets/key.png"), (20, 20))
win_img = pygame.transform.scale(pygame.image.load("assets/win.png"), (WIDTH, HEIGHT))

# Лабиринт
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Термины
terms = {
    "Stack": "LIFO структура данных",
    "Queue": "FIFO структура данных",
    "Recursion": "Функция вызывает сама себя",
    "OOP": "Объектно-ориентированное программирование",
    "Algorithm": "Набор инструкций для решения задачи",
    "Array": "Структура данных с индексированными элементами",
    "Pointer": "Переменная, содержащая адрес в памяти",
    "Lambda": "Анонимная функция в программировании",
    "Mutex": "Объект для синхронизации потоков",
    "Polymorphism": "Способность функции работать с разными типами"
}
term_keys = random.sample(list(terms.keys()), 10)

def get_valid_position():
    while True:
        x, y = random.randint(1, 18), random.randint(1, 7)
        if maze[y][x] == 0:
            return x, y

term_positions = {term: get_valid_position() for term in term_keys}

# Игрок
player_x, player_y = 1, 1
collected_terms = []

# Основной цикл
running = True
font = pygame.font.Font(None, 24)
showing_definition = None
victory = False

while running:
    screen.fill(BLACK)

    if not victory:
        # Отображение лабиринта
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                screen.blit(earth_img if cell == 0 else wall_img, (x * GRID_SIZE, y * GRID_SIZE))

        # Термины
        for term, (tx, ty) in term_positions.items():
            if term not in collected_terms:
                screen.blit(key_img, (tx * GRID_SIZE + 10, ty * GRID_SIZE + 10))

        # Игрок
        screen.blit(player_img, (player_x * GRID_SIZE, player_y * GRID_SIZE))

        # Счёт
        text = font.render(f"Terms: {len(collected_terms)}/{len(term_positions)}", True, WHITE)
        screen.blit(text, (WIDTH - 160, HEIGHT - 40))

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if showing_definition:
                    showing_definition = None
                else:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    if maze[player_y + dy][player_x + dx] == 0:
                        player_x += dx
                        player_y += dy
                    for term, (tx, ty) in term_positions.items():
                        if (tx, ty) == (player_x, player_y) and term not in collected_terms:
                            collected_terms.append(term)
                            showing_definition = f"{term}: {terms[term]}"
        # Определение
        if showing_definition:
            pygame.draw.rect(screen, WHITE, (100, 250, 600, 50))
            definition_text = font.render(showing_definition, True, BLACK)
            screen.blit(definition_text, (110, 260))

        # Победа
        if len(collected_terms) == len(term_positions):
            victory = True
            pygame.time.delay(500)
    else:
        screen.blit(win_img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10000)
        running = False

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
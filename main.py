import pygame
import random

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Maze of Terms")

# Лабиринт (1 - стена, 0 - проход)
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

# Термины и определения
terms = {"Stack": "LIFO структура данных", "Queue": "FIFO структура данных",
         "Recursion": "Функция вызывает сама себя", "OOP": "Объектно-ориентированное программирование",
         "Algorithm": "Набор инструкций для решения задачи", "Array": "Структура данных с индексированными элементами",
         "Pointer": "Переменная, содержащая адрес в памяти", "Lambda": "Анонимная функция в программировании",
         "Mutex": "Объект для синхронизации потоков", "Polymorphism": "Способность функции работать с разными типами"}
term_positions = list(terms.keys())
random.shuffle(term_positions)
term_positions = term_positions[:10]

def get_valid_position():
    while True:
        x, y = random.randint(1, 18), random.randint(1, 7)
        if maze[y][x] == 0:
            return x, y

term_objects = {name: get_valid_position() for name in term_positions}

# Игрок
player_x, player_y = 1, 1
collected_terms = []

# Основной цикл
running = True
font = pygame.font.Font(None, 24)
showing_definition = None
while running:
    screen.fill(WHITE)
    
    # Отображение лабиринта
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Отображение терминов
    for term, (tx, ty) in term_objects.items():
        if term not in collected_terms:
            pygame.draw.rect(screen, BLUE, (tx * GRID_SIZE + 10, ty * GRID_SIZE + 10, 20, 20))
    
    # Отображение игрока
    pygame.draw.rect(screen, RED, (player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Отображение счетчика
    text = font.render(f"Terms: {len(collected_terms)}/10", True, BLACK)
    screen.blit(text, (WIDTH - 120, HEIGHT - 40))
    
    # Обработка событий
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
                
                for term, (tx, ty) in term_objects.items():
                    if (tx, ty) == (player_x, player_y) and term not in collected_terms:
                        collected_terms.append(term)
                        showing_definition = f"{term}: {terms[term]}"
    
    # Отображение определения
    if showing_definition:
        definition_text = font.render(showing_definition, True, BLACK)
        pygame.draw.rect(screen, WHITE, (100, 250, 600, 50))
        screen.blit(definition_text, (110, 260))
    
    # Победа
    if len(collected_terms) == 10:
        screen.fill(WHITE)
        win_text = font.render("Win!", True, BLACK)
        screen.blit(win_text, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    
    pygame.display.flip()
    pygame.time.delay(100)

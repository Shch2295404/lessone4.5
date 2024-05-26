import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определение размеров окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Настройки ракеток и мяча
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
BALL_SPEED = 5

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game of Ping Pong')

# Определение начальных позиций ракеток и мяча
paddle1_x = 50
paddle1_y = (WINDOW_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
paddle2_x = WINDOW_WIDTH - 50 - PADDLE_WIDTH
paddle2_y = (WINDOW_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

# Определение начального счета
score1 = 0
score2 = 0

# Создание шрифта для отображения счета
font = pygame.font.Font(None, 36)

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= BALL_SPEED
    if keys[pygame.K_s] and paddle1_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        paddle1_y += BALL_SPEED
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= BALL_SPEED
    if keys[pygame.K_DOWN] and paddle2_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        paddle2_y += BALL_SPEED

    # Обновление позиции мяча
    ball_x += ball_dx
    ball_y += ball_dy

    # Проверка столкновений с верхней и нижней границами
    if ball_y <= 0 or ball_y >= WINDOW_HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Проверка столкновений с ракетками
    if (paddle1_x < ball_x < paddle1_x + PADDLE_WIDTH and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT) or \
       (paddle2_x < ball_x < paddle2_x + PADDLE_WIDTH and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Проверка выхода мяча за границы экрана
    if ball_x < 0:
        score2 += 1
        ball_x = WINDOW_WIDTH // 2
        ball_y = WINDOW_HEIGHT // 2
    elif ball_x > WINDOW_WIDTH:
        score1 += 1
        ball_x = WINDOW_WIDTH // 2
        ball_y = WINDOW_HEIGHT // 2

    # Очистка экрана
    screen.fill(BLACK)

    # Отрисовка объектов
    pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Отображение счета
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 20))

    # Обновление экрана
    pygame.display.flip()

    # Задержка для управления скоростью игры
    pygame.time.Clock().tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()

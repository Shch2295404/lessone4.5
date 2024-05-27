import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
screen_width = 800
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Survival Game")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Игрок
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]
player_color = GREEN

# Монстры
monster_size = 50
monster_colors = [RED, BLUE, (255, 255, 0)]
monsters = []

# Скорость
player_speed = 5
monster_speed = 3


# Создание начальных монстров
def create_monsters():
    for i in range(3):
        x_pos = random.randint(0, screen_width - monster_size)
        y_pos = random.randint(0, screen_height - monster_size)
        monster = {
            "pos": [x_pos, y_pos],
            "color": monster_colors[i]
        }
        monsters.append(monster)


create_monsters()

# Основной игровой цикл
run = True
while run:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Движение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
        player_pos[1] += player_speed

    # Движение монстров
    for monster in monsters:
        monster["pos"][1] += monster_speed
        if monster["pos"][1] >= screen_height:
            monster["pos"][1] = 0 - monster_size
            monster["pos"][0] = random.randint(0, screen_width - monster_size)

    # Проверка столкновений
    for monster in monsters:
        if (player_pos[0] < monster["pos"][0] < player_pos[0] + player_size or
                player_pos[0] < monster["pos"][0] + monster_size < player_pos[0] + player_size):
            if (player_pos[1] < monster["pos"][1] < player_pos[1] + player_size or
                    player_pos[1] < monster["pos"][1] + monster_size < player_pos[1] + player_size):
                run = False  # Конец игры при столкновении

    # Отрисовка
    win.fill(WHITE)
    pygame.draw.rect(win, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    for monster in monsters:
        pygame.draw.rect(win, monster["color"], (monster["pos"][0], monster["pos"][1], monster_size, monster_size))

    pygame.display.update()

pygame.quit()

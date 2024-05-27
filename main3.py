import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
screen_width = 800
screen_height = 600
play_width = 300  # 300 // 10 = 30 ширина блоков
play_height = 600  # 600 // 20 = 20 высота блоков
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

# Определение форм тетрисных фигур
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color

    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment


def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
      row = list(line)
      for j, column in enumerate(row):
        if column == '0':
            pygame.draw.rect(surface, piece.color, (sx + j * block_size, sy + i * block_size, block_size, block_size),
                             0)
            surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy - 20))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for pos in shape_pos:
          p = (pos[0], pos[1])
          if p[1] > -1:
             grid[p[1]][p[0]] = current_piece.color

        if change_piece:
          for pos in shape_pos:
             p = (pos[0], pos[1])
             locked_positions[p] = current_piece.color
          current_piece = next_piece
          next_piece = get_shape()
          change_piece = False
          score += clear_rows(grid, locked_positions) * 10

    draw_window(win, grid, score)
    draw_next_shape(next_piece, win)
    pygame.display.update()

    if check_lost(locked_positions):
        run = False
        draw_text_middle("ТЫ ПРОИГРАЛ", 80, (255, 255, 255), win)
        pygame.display.update()
        pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Нажмите любую клавишу, чтобы играть', 20, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                # Возвращаемся в меню после завершения main()
                win.fill((0, 0, 0))
                draw_text_middle('Нажмите любую клавишу, чтобы играть', 20, (255, 255, 255), win)
                pygame.display.update()
    pygame.quit()

# Инициализация Pygame
pygame.init()

# Предполагается, что screen_width и screen_height определены где-то еще в вашем коде
screen_width = 800
screen_height = 700

# Определение размеров экрана
win = pygame.display.set_mode((screen_width, screen_height))
# Установка названия окна
pygame.display.set_caption('Tetris')
# Вызов функции main_menu()
main_menu()

import pygame
import random

# Define color palette
COLORS = [
    (0, 0, 0),  # Black (empty grid)
    (150, 50, 200),  # Purple
    (90, 180, 180),  # Cyan
    (100, 50, 20),  # Brown
    (90, 140, 20),  # Green
    (200, 50, 20),  # Red
    (200, 50, 130),  # Pink
]

# Tetromino shapes and rotations
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
    [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # L
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # J
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[1, 2, 5, 6]],  # O
]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.color_index = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def get_blocks(self):
        return SHAPES[self.shape_index][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.shape_index])


class TetrisGame:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.is_active = True
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_piece = Tetromino(3, 0)
        self.next_piece = Tetromino(3, 0)

    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(3, 0)
        if self.check_collision():
            self.is_active = False

    def check_collision(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.current_piece.get_blocks():
                    if (self.current_piece.y + i >= self.rows or
                            self.current_piece.x + j < 0 or
                            self.current_piece.x + j >= self.cols or
                            self.grid[self.current_piece.y + i][self.current_piece.x + j] > 0):
                        return True
        return False

    def lock_piece(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.current_piece.get_blocks():
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color_index
        self.clear_rows()
        self.spawn_new_piece()

    def clear_rows(self):
        lines_cleared = 0
        for i in range(self.rows):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0] * self.cols)
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def move_down(self):
        self.current_piece.y += 1
        if self.check_collision():
            self.current_piece.y -= 1
            self.lock_piece()

    def move_side(self, dx):
        self.current_piece.x += dx
        if self.check_collision():
            self.current_piece.x -= dx

    def hard_drop(self):
        while not self.check_collision():
            self.current_piece.y += 1
        self.current_piece.y -= 1
        self.lock_piece()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
game = TetrisGame(20, 10)
running = True
font = pygame.font.SysFont(None, 36)


def draw_grid():
    for i in range(game.rows):
        for j in range(game.cols):
            color = COLORS[game.grid[i][j]]
            pygame.draw.rect(screen, color, (j * 20, i * 20, 20, 20), 0)
            pygame.draw.rect(screen, (128, 128, 128), (j * 20, i * 20, 20, 20), 1)


def draw_piece(piece, x_offset=0, y_offset=0):
    for i in range(4):
        for j in range(4):
            if i * 4 + j in piece.get_blocks():
                pygame.draw.rect(screen, COLORS[piece.color_index], 
                                 ((piece.x + j + x_offset) * 20, (piece.y + i + y_offset) * 20, 20, 20), 0)
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((piece.x + j + x_offset) * 20, (piece.y + i + y_offset) * 20, 20, 20), 1)


def draw_next_piece():
    pygame.draw.rect(screen, (255, 255, 255), (220, 50, 100, 100), 2)
    draw_piece(game.next_piece, x_offset=11, y_offset=2)
    text = font.render("Next", True, (255, 255, 255))
    screen.blit(text, (230, 20))


def display_score():
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    screen.blit(score_text, (220, 180))


while running:
    screen.fill((0, 0, 0))
    draw_grid()
    draw_piece(game.current_piece)
    draw_next_piece()
    display_score()

    if not game.is_active:
        text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(text, (100, 250))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_side(-1)
            elif event.key == pygame.K_RIGHT:
                game.move_side(1)
            elif event.key == pygame.K_DOWN:
                game.move_down()
            elif event.key == pygame.K_SPACE:
                game.hard_drop()
            elif event.key == pygame.K_UP:
                game.current_piece.rotate()

    game.move_down()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

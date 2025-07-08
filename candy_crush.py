import pygame
import random
import sys

# === CONFIG ===
GRID_SIZE = 8
CANDY_TYPES = 6
TILE_SIZE = 64
WIDTH, HEIGHT = TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE + 80
FPS = 60

# === COLORS ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CANDY_COLORS = [
    (255, 85, 85),     # red
    (255, 255, 100),   # yellow
    (100, 255, 100),   # green
    (100, 100, 255),   # blue
    (200, 100, 255),   # purple
    (255, 170, 0)      # orange
]

# === INITIALIZE ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# === BOARD ===
def random_candy():
    return random.randint(0, CANDY_TYPES - 1)

def create_board():
    return [[random_candy() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

board = create_board()
score = 0

# === DRAWING ===
def draw_board():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            candy = board[row][col]
            color = CANDY_COLORS[candy]
            rect = pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

def draw_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, HEIGHT - 70))

# === MATCHING ===
def find_matches():
    matches = set()

    # horizontal
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 2):
            if board[r][c] == board[r][c+1] == board[r][c+2]:
                matches.update({(r, c), (r, c+1), (r, c+2)})
    
    # vertical
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 2):
            if board[r][c] == board[r+1][c] == board[r+2][c]:
                matches.update({(r, c), (r+1, c), (r+2, c)})

    return matches

def collapse_board():
    global score
    matches = find_matches()
    if not matches:
        return False

    score += len(matches) * 10

    # Remove matched candies
    for r, c in matches:
        board[r][c] = None

    # Drop candies
    for c in range(GRID_SIZE):
        col = [board[r][c] for r in range(GRID_SIZE)]
        col = [candy for candy in col if candy is not None]
        col = [None]*(GRID_SIZE - len(col)) + col
        for r in range(GRID_SIZE):
            board[r][c] = col[r]

    # Fill new candies
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] is None:
                board[r][c] = random_candy()

    return True

# === SWAPPING ===
def get_grid_pos(x, y):
    return y // TILE_SIZE, x // TILE_SIZE

def is_adjacent(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2) == 1

def swap(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

# === GAME LOOP ===
selected = None
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < GRID_SIZE * TILE_SIZE:
                selected = get_grid_pos(x, y)

        elif event.type == pygame.MOUSEBUTTONUP and selected:
            x, y = pygame.mouse.get_pos()
            released = get_grid_pos(x, y)
            if is_adjacent(selected, released):
                swap(selected, released)
                if not find_matches():
                    swap(selected, released)  # invalid move, revert
            selected = None

    while collapse_board():
        pygame.time.delay(100)

    draw_board()
    draw_score()
    pygame.display.flip()

pygame.quit()
sys.exit()

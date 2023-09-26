import pygame
import sys
import random
from collections import deque

# Configurações
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
NUM_ROWS = HEIGHT // GRID_SIZE
NUM_COLS = WIDTH // GRID_SIZE
MINES = {
    "Fácil": 30,
    "Média": 50,
    "Difícil": 99,
    "Impossível": 180
}
MINE = -1

# Estados do jogo
MENU = "menu"
PLAYING = "playing"
current_state = MENU  # Estado inicial
current_difficulty = None  # Dificuldade selecionada


# Cores
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Inicialização do pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo Minado")

# Função para criar o tabuleiro
def create_board():
    if current_difficulty:
        NUM_MINES = MINES[current_difficulty]
    else:
        NUM_MINES = 40
    board = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    mines = random.sample(range(NUM_COLS * NUM_ROWS), NUM_MINES)
    for mine in mines:
        x, y = mine % NUM_COLS, mine // NUM_COLS
        board[y][x] = MINE
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < NUM_COLS and 0 <= y + dy < NUM_ROWS and board[y + dy][x + dx] != MINE:
                    board[y + dy][x + dx] += 1
    return board

def game_over_message():
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Função para revelar células vazias e seus vizinhos com números usando BFS
def bfs_reveal(board, revealed, x, y):
    queue = deque([(x, y)])
    revealed[y][x] = True

    while queue:
        cx, cy = queue.popleft()

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < NUM_COLS and 0 <= ny < NUM_ROWS and not revealed[ny][nx]:
                    revealed[ny][nx] = True
                    if board[ny][nx] == 0:
                        queue.append((nx, ny))

# Função para desenhar o tabuleiro
def draw_board(board, revealed):
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Adicionando bordas
            if revealed[y][x]:
                if board[y][x] == MINE:
                    pygame.draw.circle(screen, BLACK, rect.center, GRID_SIZE // 2)
                elif board[y][x] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(board[y][x]), True, BLUE)  # Cor dos números
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)  # Cor das células vazias

# Função para exibir a mensagem de vitória
def victory_message():
    font = pygame.font.Font(None, 48)
    text = font.render("Você venceu!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

"""def toggle_show_bfs(show_bfs):
    font = pygame.font.Font(None, 24)
    if show_bfs:
        text = font.render("Mostrar BFS em Tempo Real: Ativado", True, BLACK)
    else:
        text = font.render("Mostrar BFS em Tempo Real: Desativado", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    screen.blit(text, text_rect)
"""

def show_difficulty_menu():
    global current_state, current_difficulty
    font = pygame.font.Font(None, 36)
    text = font.render("Selecione a Dificuldade:", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text, text_rect)

    button_rects = []
    for idx, (difficulty, num_mines) in enumerate(MINES.items()):
        button_rect = pygame.Rect(
            WIDTH // 4,
            HEIGHT // 2 + idx * 50,
            WIDTH // 2,
            40
        )
        pygame.draw.rect(screen, GRAY, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 1)
        text = font.render(difficulty, True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        button_rects.append((button_rect, difficulty, num_mines))

    pygame.display.flip()

    while current_state == MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for button_rect, difficulty, num_mines in button_rects:
                    if button_rect.collidepoint(x, y):
                        current_difficulty = difficulty
                        current_state = PLAYING

# Função principal do jogo
def main():
    global current_state, current_difficulty
    while True:
        if current_state == MENU:
            show_difficulty_menu()

        if current_state == PLAYING:
            board = create_board()
            revealed = [[False for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

        game_over = False
        victory = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    x //= GRID_SIZE
                    y //= GRID_SIZE
                    if not revealed[y][x]:
                        if board[y][x] == 0:
                            bfs_reveal(board, revealed, x, y)
                        else:
                            revealed[y][x] = True
                            if board[y][x] == MINE:
                                game_over = True

            screen.fill(GRAY)
            draw_board(board, revealed)

            pygame.display.flip()

            # Verifique a vitória
            victory = all(all(revealed[y][x] or board[y][x] == MINE for x in range(NUM_COLS)) for y in range(NUM_ROWS) for x in range(NUM_COLS) if board[y][x] != MINE)

            if victory:
                game_over = True

        if victory:
            victory_message()
        else:
            game_over_message()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()

import tkinter as tk
import random
from queue import Queue

# Dimensões do campo minado
ROWS, COLS = 10, 10
MINE_COUNT = 20

# Cores
UNEXPLORED_COLOR = "gray"
EXPLORED_COLOR = "lightgray"
MINE_COLOR = "red"
FONT_SIZE = 12

def create_minefield():
    minefield = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    mines = random.sample(range(ROWS * COLS), MINE_COUNT)

    for mine in mines:
        row = mine // COLS
        col = mine % COLS
        minefield[row][col] = "X"

    return minefield

def count_adjacent_mines(minefield, row, col):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and minefield[r][c] == "X":
                count += 1
    return count

def bfs_explore(minefield, row, col):
    if minefield[row][col] != " ":
        return

    minefield[row][col] = str(count_adjacent_mines(minefield, row, col))

    if minefield[row][col] == "0":
        queue = Queue()
        queue.put((row, col))

        while not queue.empty():
            r, c = queue.get()
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and minefield[nr][nc] == " ":
                        minefield[nr][nc] = str(count_adjacent_mines(minefield, nr, nc))
                        if minefield[nr][nc] == "0":
                            queue.put((nr, nc))

def reveal_minefield(row, col):
    if minefield[row][col] == "X":
        game_over_label.config(text="Game Over!", fg="red")
        reveal_all_mines()
    else:
        bfs_explore(minefield, row, col)
        update_display()

def reveal_all_mines():
    for r in range(ROWS):
        for c in range(COLS):
            if minefield[r][c] == "X":
                mine_buttons[r][c].config(text="X", bg=MINE_COLOR)
            else:
                mine_buttons[r][c].config(state="disabled")

def update_display():
    for r in range(ROWS):
        for c in range(COLS):
            if minefield[r][c] != " ":
                mine_buttons[r][c].config(text=minefield[r][c], state="disabled", bg=EXPLORED_COLOR)

def button_click(row, col):
    if not game_over:
        reveal_minefield(row, col)
        check_win_condition()

def check_win_condition():
    if all(minefield[r][c] != " " or minefield[r][c] == "X" for r in range(ROWS) for c in range(COLS)):
        game_over_label.config(text="You Win!", fg="green")

# Criação do campo minado
minefield = create_minefield()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Campo Minado")

mine_buttons = []

for r in range(ROWS):
    row_buttons = []
    for c in range(COLS):
        button = tk.Button(root, text=" ", font=("Helvetica", FONT_SIZE), width=2, height=1,
                           command=lambda row=r, col=c: button_click(row, col))
        button.grid(row=r, column=c)
        row_buttons.append(button)
    mine_buttons.append(row_buttons)

game_over = False
game_over_label = tk.Label(root, text="", font=("Helvetica", FONT_SIZE))
game_over_label.grid(row=ROWS, columnspan=COLS)

root.mainloop()

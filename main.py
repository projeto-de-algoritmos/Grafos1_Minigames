import tkinter as tk
from tkinter import messagebox

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_win(board, player):
    # Verifica se o jogador venceu nas linhas, colunas ou diagonais.
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    # Verifica se o jogo empatou (tabuleiro cheio).
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def minimax(board, depth, maximizing_player):
    scores = {"X": -1, "O": 1, "draw": 0}
    player = "O" if maximizing_player else "X"

    if check_win(board, "O"):
        return scores["O"]
    if check_win(board, "X"):
        return scores["X"]
    if check_draw(board):
        return scores["draw"]

    if maximizing_player:
        max_eval = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    best_move = None
    best_eval = float("-inf")
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                eval = minimax(board, 0, False)
                board[i][j] = " "
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

def make_move(row, col):
    global board, currentPlayer, game_over

    if board[row][col] == " " and not game_over:
        board[row][col] = currentPlayer
        buttons[row][col].config(text=currentPlayer, state="disabled")

        if check_win(board, currentPlayer):
            messagebox.showinfo("Fim de jogo", f"Jogador {currentPlayer} ganhou!")
            game_over = True
        elif check_draw(board):
            messagebox.showinfo("Fim de jogo", "Empate!")
            game_over = True
        else:
            currentPlayer = "X" if currentPlayer == "O" else "O"
            if currentPlayer == "O" and not game_over:
                row, col = find_best_move(board)
                make_move(row, col)

app = tk.Tk()
app.title("Jogo da Velha")

currentPlayer = "X"
game_over = False
board = create_board()
buttons = []

for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(app, text=" ", font=("Helvetica", 24), width=6, height=3,
                           command=lambda row=i, col=j: make_move(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

app.mainloop()

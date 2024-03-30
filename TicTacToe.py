import tkinter as tk
from tkinter import messagebox

def game_over(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ' or board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    for row in board:
        if ' ' in row:
            return False
    return True

def evaluate(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == 'X':
                return 1
            elif board[row][0] == 'O':
                return -1

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return 1
            elif board[0][col] == 'O':
                return -1

    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] == 'X':
            return 1
        elif board[1][1] == 'O':
            return -1

    if not any(' ' in row for row in board):
        return 0  # Tie
    return None  # Game not finished

def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)
    if score is not None:
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move(board):
    best_score = float('-inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.initialize_board()

    def initialize_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                                               command=lambda row=i, col=j: self.player_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        self.initialize_board()

    def player_move(self, row, col):
        if self.board[row][col] == ' ' and not game_over(self.board):
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O')
            if game_over(self.board):
                self.end_game()
                return
            self.ai_move()

    def ai_move(self):
        move = best_move(self.board)
        if move:
            self.board[move[0]][move[1]] = 'X'
            self.buttons[move[0]][move[1]].config(text='X')
            if game_over(self.board):
                self.end_game()

    def end_game(self):
        result = evaluate(self.board)
        if result == 1:
            messagebox.showinfo("Game Over", "AI wins!")
        elif result == -1:
            messagebox.showinfo("Game Over", "You win!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state='disabled')
        if messagebox.askyesno("Game Over", "Would you like to play again?"):
            self.reset_board()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    TicTacToeGUI(root)
    root.mainloop()

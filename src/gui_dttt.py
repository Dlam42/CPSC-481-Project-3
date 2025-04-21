import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 3
DISAPPEAR_AFTER = 4

class Game:
    def __init__(self):
        self.board = [[' ']*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.history = []  # stores (row, col, player, turn)
        self.turn_count = 0

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.history.append((row, col, player, self.turn_count))
            self.turn_count += 1
            self.expire_old_moves()
            return True
        return False

    def expire_old_moves(self):
        to_remove = [m for m in self.history if self.turn_count - m[3] >= DISAPPEAR_AFTER]
        for r, c, _, _ in to_remove:
            self.board[r][c] = ' '
        self.history = [m for m in self.history if self.turn_count - m[3] < DISAPPEAR_AFTER]

    def is_winner(self, p):
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == p for j in range(BOARD_SIZE)) or \
               all(self.board[j][i] == p for j in range(BOARD_SIZE)):
                return True
        if all(self.board[i][i] == p for i in range(BOARD_SIZE)) or \
           all(self.board[i][BOARD_SIZE-1-i] == p for i in range(BOARD_SIZE)):
            return True
        return False

    def is_full(self):
        return all(self.board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

    def get_empty_cells(self):
        return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == ' ']

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for (i, j) in self.get_empty_cells():
            # Backup
            board_backup = [row[:] for row in self.board]
            hist_backup = self.history[:]
            turn_backup = self.turn_count

            self.board[i][j] = 'O'
            self.history.append((i, j, 'O', self.turn_count))
            self.turn_count += 1
            self.expire_old_moves()

            score = self.minimax(0, False)

            # Restore
            self.board = [row[:] for row in board_backup]
            self.history = hist_backup[:]
            self.turn_count = turn_backup

            if score > best_score:
                best_score = score
                best_move = (i, j)

        if best_move:
            self.make_move(best_move[0], best_move[1], 'O')
        return best_move

    def minimax(self, depth, is_maximizing):
        if self.is_winner('O'):
            return 10 - depth
        if self.is_winner('X'):
            return depth - 10
        if self.is_full():
            return 0

        board_backup = [row[:] for row in self.board]
        hist_backup = self.history[:]
        turn_backup = self.turn_count

        if is_maximizing:
            max_eval = float('-inf')
            for (i, j) in self.get_empty_cells():
                self.board[i][j] = 'O'
                self.history.append((i, j, 'O', self.turn_count))
                self.turn_count += 1
                self.expire_old_moves()
                eval = self.minimax(depth + 1, False)
                self.board = [row[:] for row in board_backup]
                self.history = hist_backup[:]
                self.turn_count = turn_backup
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for (i, j) in self.get_empty_cells():
                self.board[i][j] = 'X'
                self.history.append((i, j, 'X', self.turn_count))
                self.turn_count += 1
                self.expire_old_moves()
                eval = self.minimax(depth + 1, True)
                self.board = [row[:] for row in board_backup]
                self.history = hist_backup[:]
                self.turn_count = turn_backup
                min_eval = min(min_eval, eval)
            return min_eval

class GUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.buttons = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.build_gui()

    def build_gui(self):
        self.root.title("Disappearing Tic-Tac-Toe")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(self.root, text=' ', font=('Arial', 40), width=3, height=1,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, row, col):
        if self.game.make_move(row, col, 'X'):
            self.refresh_board()
            if self.check_end('X'):
                return
            ai_pos = self.game.ai_move()
            self.refresh_board()
            if self.check_end('O'):
                return

    def refresh_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j]['text'] = self.game.board[i][j]

    def check_end(self, player):
        if self.game.is_winner(player):
            messagebox.showinfo("Game Over", f"{'You' if player == 'X' else 'AI'} wins!")
            self.root.quit()
            return True
        elif self.game.is_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.root.quit()
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

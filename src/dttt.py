# disappearing_ttt.py

BOARD_SIZE = 3
DISAPPEAR_AFTER = 4  # Moves disappear after 4 turns

class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.history = []  # Stores (row, col, player, turn_num)
        self.turn_count = 0

    def display(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.history.append((row, col, player, self.turn_count))
            self.turn_count += 1
            self.expire_old_moves()
            return True
        return False

    def expire_old_moves(self):
        to_remove = [move for move in self.history if self.turn_count - move[3] >= DISAPPEAR_AFTER]
        for row, col, _, _ in to_remove:
            self.board[row][col] = ' '
        self.history = [m for m in self.history if self.turn_count - m[3] < DISAPPEAR_AFTER]

    def is_winner(self, player):
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)) or \
               all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                return True
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)) or \
           all(self.board[i][BOARD_SIZE-1-i] == player for i in range(BOARD_SIZE)):
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
            # Try move
            self.board[i][j] = 'O'
            self.history.append((i, j, 'O', self.turn_count))
            self.turn_count += 1
            self.expire_old_moves()

            score = self.minimax(0, False)

            # Undo move
            self.board[i][j] = ' '
            self.turn_count -= 1
            self.history.pop()

            if score > best_score:
                best_score = score
                best_move = (i, j)

        if best_move:
            self.make_move(best_move[0], best_move[1], 'O')

    def minimax(self, depth, is_maximizing):
        if self.is_winner('O'):
            return 10 - depth
        if self.is_winner('X'):
            return depth - 10
        if self.is_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for (i, j) in self.get_empty_cells():
                self.board[i][j] = 'O'
                self.history.append((i, j, 'O', self.turn_count))
                self.turn_count += 1
                self.expire_old_moves()

                eval = self.minimax(depth + 1, False)

                self.board[i][j] = ' '
                self.turn_count -= 1
                self.history.pop()
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

                self.board[i][j] = ' '
                self.turn_count -= 1
                self.history.pop()
                min_eval = min(min_eval, eval)
            return min_eval


def main():
    game = Game()
    print("Welcome to Disappearing Tic-Tac-Toe (X = You, O = AI)")
    game.display()

    while True:
        # Human move
        while True:
            try:
                move = input("Enter your move (row col, 0-2): ")
                row, col = map(int, move.strip().split())
                if 0 <= row <= 2 and 0 <= col <= 2 and game.make_move(row, col, 'X'):
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter valid row and column numbers (0-2).")

        game.display()
        if game.is_winner('X'):
            print("You win!")
            break
        if game.is_full():
            print("It's a tie!")
            break

        # AI move
        print("AI is thinking...\n")
        game.ai_move()
        game.display()
        if game.is_winner('O'):
            print("AI wins!")
            break
        if game.is_full():
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()

class DisappearingTicTacToe:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = 0
        self.winner = None
        self.move_history = {'X': [], 'O': []}  # Each entry: (row, col)

    def count_player_moves(self, player):
        return len(self.move_history[player])

    def make_move(self, row, col, player):
        if self.winner:
            return False

        if (row, col) not in self.get_valid_moves():
            print(f"Move invalid: not in valid_moves list.")
            return False

        # Remove oldest if player already has 3 moves
        if len(self.move_history[player]) >= 3:
            old_row, old_col = self.move_history[player].pop(0)
            self.board[old_row][old_col] = None

        move_number = len(self.move_history[player]) + 1
        self.board[row][col] = [player, self.current_turn, move_number]
        self.move_history[player].append((row, col))

        visible_board = self.get_visible_board(self.current_turn)
        if self.check_win(visible_board, player):
            self.winner = player

        self.current_turn += 1
        return True

    def get_valid_moves(self):
        moves = []
        if self.winner is None:
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        moves.append((r, c))
        return moves

    def get_visible_board(self, turn_number=None):
        if turn_number is None:
            turn_number = self.current_turn

        visible_board = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                if cell:
                    player, turn_placed, move_number = cell
                    visible_board[r][c] = [player, turn_placed, move_number]
        return visible_board

    def check_win(self, board, player):
        for i in range(3):
            if all(board[i][j] and board[i][j][0] == player for j in range(3)):
                return True
            if all(board[j][i] and board[j][i][0] == player for j in range(3)):
                return True
        if all(board[i][i] and board[i][i][0] == player for i in range(3)):
            return True
        if all(board[i][2 - i] and board[i][2 - i][0] == player for i in range(3)):
            return True
        return False

    def is_game_over(self):
        return self.winner is not None


class DisappearingTicTacToe:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = 0
        self.winner = None

    def count_player_moves(self, player):
        return sum(
            1 for r in range(3) for c in range(3)
            if self.board[r][c] and self.board[r][c][0] == player
        )

    def make_move(self, row, col, player):
        if self.winner:
            return False

        if (row, col) not in self.get_valid_moves():
            print(f"Move invalid: not in valid_moves list.")
            return False

        move_number = self.count_player_moves(player) + 1
        self.board[row][col] = [player, self.current_turn, move_number]
        self.current_turn += 1

        visible_board = self.get_visible_board(self.current_turn)
        if self.check_win(visible_board, player):
            self.winner = player
        return True

    def get_valid_moves(self):
        """Returns a list of (row, col) tuples for valid empty or expired cells."""
        moves = []
        if self.winner is None:
            for r in range(3):
                for c in range(3):
                    cell = self.board[r][c]
                    if cell is None:
                        moves.append((r, c))
                    else:
                        player, _, move_number = cell
                        player_moves_so_far = self.count_player_moves(player)
                        if player_moves_so_far >= move_number + 3:
                            # Piece has expired, slot is now valid
                            moves.append((r, c))
        return moves


    def get_visible_board(self, turn_number=None):
        if turn_number is None:
            turn_number = self.current_turn

        visible_board = [[None for _ in range(3)] for _ in range(3)]

        # Count how many moves each player has made
        move_counts = {'X': 0, 'O': 0}
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                if cell:
                    player, _, _ = cell
                    move_counts[player] += 1

        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                if cell:
                    player, _, move_number = cell
                    # Keep this move visible if it's within the last 3 moves of that player
                    if move_counts[player] - move_number < 3:
                        visible_board[r][c] = [player, _, move_number]

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

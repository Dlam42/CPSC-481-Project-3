# game_engine.py
import copy

# --- Player Constants (Optional, but good practice) ---
# These could also be defined in ai_player.py or a central config
HUMAN_PLAYER = 'X'
AI_PLAYER = 'O'

class DisappearingTicTacToe:
    """
    Represents the Disappearing Tic-Tac-Toe game state and logic.
    Pieces disappear 3 turns after they are placed (invisible at the start of turn_placed + 3).
    """
    def __init__(self):
        """Initializes the game board, turn counter, and winner status."""
        # Board stores tuples: (player, turn_placed) or None
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = 1
        self.winner = None # None, 'X', 'O', or 'Draw'

    def current_player(self):
        """Determines the current player based on the turn number."""
        if self.current_turn % 2 == 1:
            return HUMAN_PLAYER # Assuming Human ('X') starts
        else:
            return AI_PLAYER # AI ('O') plays second

    def get_visible_board(self, turn_number=None):
        if turn_number is None:
           turn_number = self.current_turn

        visible_board = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                cell = self.board[r][c]
                if cell:
                    player, turn_placed, move_number = cell

                    # Count how many turns this player has taken up to now
                    current_player_moves = sum(
                        1 for row in self.board for c in row if c and c[0] == player
                    )

                    # Disappear if player has made 4+ moves since this one
                    if current_player_moves < move_number + 3:
                        visible_board[r][c] = player
        return visible_board 


    def get_valid_moves(self):
        """Returns a list of (row, col) tuples for valid empty cells."""
        moves = []
        if self.winner is None:
            for r in range(3):
                for c in range(3):
                    # A move is valid if the cell is actually empty (None)
                    if self.board[r][c] is None:
                        moves.append((r, c))
        return moves

    def make_move(self, row, col, player):
        """
        Attempts to place a player's piece on the board at (row, col).
        Updates the game state (board, current_turn, winner).
        Returns True if the move was successful, False otherwise.
        """
        # Check if move is valid: cell is empty and game is not over
        if self.winner is not None:
            print("Error: Game is already over.")
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
             print(f"Error: Move ({row}, {col}) is outside board boundaries.")
             return False
        if self.board[row][col] is not None:
            print(f"Error: Cell ({row}, {col}) is already occupied.")
            return False
        # Check if it's the correct player's turn
        if player != self.current_player():
             print(f"Error: It's not Player {player}'s turn (Current: {self.current_player()}).")
             return False


        # Place the piece along with the current turn number
        # Count how many moves this player has made so far
        player_move_number = sum(
            1 for r in self.board for cell in r if cell and cell[0] == player
        ) + 1  # +1 for the current move

        self.board[row][col] = (player, self.current_turn, player_move_number)


        # Determine the board state visible *after* this move for win/draw check
        # This looks at the board state as it will be at the START of the next turn
        visible_board_after_move = self.get_visible_board(self.current_turn + 1)

        # Check for win
        if self.check_win(visible_board_after_move, player):
            self.winner = player
        # Check for draw (only if no winner)
        # Pass the *current* turn's visibility check + valid moves check
        elif self.is_draw():
             self.winner = "Draw"

        # Increment turn number only if the move was successfully placed
        self.current_turn += 1
        return True # Move successful

    def check_win(self, visible_board, player):
        """Checks if the given player has won on the visible board state."""
        # Check rows
        for r in range(3):
            if all(visible_board[r][c] == player for c in range(3)):
                return True
        # Check columns
        for c in range(3):
            if all(visible_board[r][c] == player for r in range(3)):
                return True
        # Check diagonals
        if all(visible_board[i][i] == player for i in range(3)):
            return True
        if all(visible_board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
         """
         Checks if the game is a draw.
         Conditions: No winner AND no valid moves left on the actual board.
         """
         # If someone has already won, it's not a draw
         if self.winner is not None and self.winner != "Draw":
             return False

         # If there are no more valid moves possible on the actual board
         if not self.get_valid_moves():
             # Check if the current visible state has a winner
            visible_board = self.get_visible_board(self.current_turn)
            if not self.check_win(visible_board, HUMAN_PLAYER) and \
               not self.check_win(visible_board, AI_PLAYER):
                 return True # No moves left, no winner -> Draw

         return False

    def is_game_over(self):
        """Checks if the game has ended (win or draw). Recalculates draw if needed."""
        if self.winner is None:
             # Explicitly check draw condition based on current state
             if self.is_draw():
                  self.winner = "Draw"
        return self.winner is not None

    def print_board(self, turn_to_display=None):
        """Prints the current *visible* board state to the console."""
        if turn_to_display is None:
            turn_to_display = self.current_turn
        visible_board = self.get_visible_board(turn_to_display)
        print(f"\nBoard at start of Turn {turn_to_display}:")
        print("-" * 13)
        for row in visible_board:
            print("|", end="")
            for cell in row:
                print(f" {cell if cell is not None else ' '} |", end="")
            print("\n" + "-" * 13)
        if self.winner:
            print(f"Game Over! Winner: {self.winner}")
        # Print current turn only if game is not over
        elif not self.is_game_over():
             print(f"Current Turn: {self.current_turn} (Player {self.current_player()})")


    def get_state_copy(self):
        """Returns a deep copy of the current game state."""
        new_game = DisappearingTicTacToe()
        new_game.board = copy.deepcopy(self.board)
        new_game.current_turn = self.current_turn
        new_game.winner = self.winner
        return new_game
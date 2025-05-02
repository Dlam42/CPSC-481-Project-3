from copy import deepcopy

class AIPlayer:
    def __init__(self, player_symbol):
        self.player = player_symbol
        self.opponent = "O" if player_symbol == "X" else "X"

    def get_best_move(self, game_state):
        best_score = float('-inf')
        best_move = None

        for move in game_state.get_valid_moves():
            game_copy = deepcopy(game_state)
            game_copy.make_move(move[0], move[1], self.player)
            score = self.minimax(game_copy, False, depth=1)  # Start at depth 1

            if score > best_score:
                best_score = score
                best_move = move

        return best_move


    def minimax(self, game_state, is_maximizing, depth=0, max_depth=3):
        if game_state.is_game_over() or depth == max_depth:
            if game_state.winner == self.player:
                return 1
            elif game_state.winner == self.opponent:
                return -1
            return 0  # No winner

        best_score = float('-inf') if is_maximizing else float('inf')
        for move in game_state.get_valid_moves():
            game_copy = deepcopy(game_state)
            game_copy.make_move(move[0], move[1], self.player if is_maximizing else self.opponent)
            score = self.minimax(game_copy, not is_maximizing, depth + 1, max_depth)

            if is_maximizing:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)

        return best_score

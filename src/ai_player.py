# ai_player.py
import math
# Assuming DisappearingTicTacToe class is in game_engine.py
# from game_engine import DisappearingTicTacToe # Not needed directly in functions, but for context

# --- AI Constants ---
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

def minimax(game_state, depth, is_maximizing_player):
    """
    Recursive minimax function.
    Args:
        game_state: A copy of the DisappearingTicTacToe game state.
        depth: Current depth in the game tree (optional, can be used for limits).
        is_maximizing_player: Boolean, True if evaluating for AI ('O'), False for Human ('X').

    Returns:
        The score (+1 for AI win, -1 for Human win, 0 for Draw) of the state.
    """

    # --- Base Cases: Check if the game ended AFTER the last move ---
    # Check the winner attribute determined by game_state.make_move
    if game_state.winner == AI_PLAYER:
        return 1
    elif game_state.winner == HUMAN_PLAYER:
        return -1
    elif game_state.winner == "Draw":
        return 0

    # Added check: if no moves left and game state says no winner yet,
    # re-check draw explicitly as make_move might not have caught it
    # if the last move didn't immediately fill the visible board.
    if not game_state.get_valid_moves():
        if game_state.is_draw(): # is_draw checks win condition again
            return 0
        else:
            # This case should be rare if is_draw is correct, but indicates an issue
            # Maybe return a neutral score or handle based on final board state.
             print("Warning: No valid moves but not detected as win/draw in minimax base case.")
             return 0


    # --- Recursive Step ---
    valid_moves = game_state.get_valid_moves()

    if is_maximizing_player: # AI's turn ('O') - maximize the score
        max_eval = -math.inf
        for r, c in valid_moves:
            state_copy = game_state.get_state_copy()
            # Check if move is valid for the player whose turn it is in the copy
            if state_copy.current_player() == AI_PLAYER:
                 if state_copy.make_move(r, c, AI_PLAYER):
                    evaluation = minimax(state_copy, depth + 1, False) # Next turn is minimizing (human)
                    max_eval = max(max_eval, evaluation)
                 else:
                      print(f"Minimax (Max): AI failed to make valid move {r},{c} on copy?") # Should not happen often
            else:
                 print(f"Minimax (Max): Turn mismatch? Expected {AI_PLAYER}, got {state_copy.current_player()}")
        return max_eval
    else: # Human's turn ('X') - minimize the score (from AI's perspective)
        min_eval = math.inf
        for r, c in valid_moves:
            state_copy = game_state.get_state_copy()
            # Check if move is valid for the player whose turn it is in the copy
            if state_copy.current_player() == HUMAN_PLAYER:
                if state_copy.make_move(r, c, HUMAN_PLAYER):
                    evaluation = minimax(state_copy, depth + 1, True) # Next turn is maximizing (AI)
                    min_eval = min(min_eval, evaluation)
                else:
                      print(f"Minimax (Min): Human failed to make valid move {r},{c} on copy?") # Should not happen often
            else:
                print(f"Minimax (Min): Turn mismatch? Expected {HUMAN_PLAYER}, got {state_copy.current_player()}")

        # Handle case where min_eval remains infinity (e.g., no valid moves explored?)
        return min_eval if min_eval != math.inf else 0


def find_best_move(game_state):
    """
    Finds the best move for the AI player ('O') using Minimax.
    Args:
        game_state: The current DisappearingTicTacToe game state.

    Returns:
        A tuple (row, col) representing the best move, or None if no moves are possible.
    """
    best_score = -math.inf
    best_move = None
    valid_moves = game_state.get_valid_moves()

    if not valid_moves:
        print("AI: No valid moves found.")
        return None # No moves left

    print(f"AI evaluating moves: {valid_moves}")

    for r, c in valid_moves:
        state_copy = game_state.get_state_copy()
        # Simulate AI making the move
        if state_copy.make_move(r, c, AI_PLAYER):
            # Evaluate the state *after* the AI's move, assuming human plays next (minimizing)
            move_score = minimax(state_copy, 0, False) # Depth 0, next player is minimizing (Human)
            print(f"  Move ({r},{c}) evaluated score: {move_score}")

            # If this move's score is better than the best score found so far
            # In case of ties, this favors the first best move found.
            if move_score > best_score:
                best_score = move_score
                best_move = (r, c)
        else:
             print(f"AI: Error simulating move ({r},{c}) in find_best_move")


    # If no move improved score (e.g., all lead to loss), pick the first valid move?
    if best_move is None and valid_moves:
         print("AI: No move improved score, picking first valid move.")
         best_move = valid_moves[0]

    print(f"AI best move found: {best_move} with score {best_score}")
    return best_move
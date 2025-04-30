from flask import Flask, request, jsonify, render_template
import math
import copy

from game_engine import DisappearingTicTacToe
from ai_player import find_best_move, AI_PLAYER, HUMAN_PLAYER

app = Flask(__name__)
game = DisappearingTicTacToe()

# --- Helper function ---
def convert_board_to_json_compatible(board):
    """Convert tuple-based board to list-of-lists for frontend JSON."""
    json_board = [[list(cell) if cell else None for cell in row] for row in board]
    print("Sending board to frontend:")
    for row in json_board:
        print(row)
    return json_board

# --- Routes ---
@app.route('/')
def index():
    global game
    game = DisappearingTicTacToe()  # Reset on page load
    return render_template('index.html')


@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = DisappearingTicTacToe()
    return jsonify({
        'message': 'Game reset.',
        'full_board': convert_board_to_json_compatible(game.board),
        'current_turn': game.current_turn,
        'game_over': False,
        'winner': None,
        'current_player': game.current_player()
    })


@app.route('/move', methods=['POST'])
def handle_move():
    global game

    print("-" * 30)
    print(f"Received /move request at Turn {game.current_turn}")
    print(f"Current player: {game.current_player()} | Winner: {game.winner}")
    print("Valid moves:", game.get_valid_moves())

    data = request.json
    row, col = data.get('row'), data.get('col')
    print(f"Human attempted move at: ({row}, {col})")

    if game.is_game_over():
        return jsonify({
            'error': 'Game is already over.',
            'full_board': convert_board_to_json_compatible(game.board),
            'current_turn': game.current_turn,
            'game_over': True,
            'winner': game.winner,
            'current_player': game.current_player()
        }), 400

    if game.current_player() == HUMAN_PLAYER:
        if (row, col) not in game.get_valid_moves():
            print("Move invalid: not in valid_moves list.")
            return jsonify({
                'error': 'Invalid move.',
                'full_board': convert_board_to_json_compatible(game.board),
                'current_turn': game.current_turn,
                'game_over': game.is_game_over(),
                'winner': game.winner,
                'current_player': game.current_player()
            }), 400

        move_successful = game.make_move(row, col, HUMAN_PLAYER)
        print(f"Human move successful? {move_successful}")
        if not move_successful:
            return jsonify({
                'error': 'Failed to make human move.',
                'full_board': convert_board_to_json_compatible(game.board),
                'current_turn': game.current_turn,
                'game_over': game.is_game_over(),
                'winner': game.winner,
                'current_player': game.current_player()
            }), 500
    else:
        print("Invalid move: not human's turn.")
        return jsonify({
            'error': "Not your turn.",
            'full_board': convert_board_to_json_compatible(game.board),
            'current_turn': game.current_turn,
            'game_over': game.is_game_over(),
            'winner': game.winner,
            'current_player': game.current_player()
        }), 400

    # AI Move
    if not game.is_game_over():
        ai_move = find_best_move(game.get_state_copy())
        if ai_move:
            print(f"AI selects move: {ai_move}")
            game.make_move(ai_move[0], ai_move[1], AI_PLAYER)

    # Final response
    return jsonify({
        'message': 'Move completed.',
        'full_board': convert_board_to_json_compatible(game.board),
        'current_turn': game.current_turn,
        'game_over': game.is_game_over(),
        'winner': game.winner,
        'current_player': game.current_player()
    }), 200


if __name__ == '__main__':
    app.run(debug=True)

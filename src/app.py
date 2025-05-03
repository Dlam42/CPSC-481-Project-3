from flask import Flask, render_template, request, jsonify
from game_engine import DisappearingTicTacToe
from ai_player import AIPlayer

app = Flask(__name__, static_url_path="/static")
game = DisappearingTicTacToe()
ai = AIPlayer("O")

HUMAN_PLAYER = "X"
AI_PLAYER = "O"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    game.reset_game()
    return jsonify({"status": "Game reset."})

@app.route("/move", methods=["POST"])
def handle_move():
    data = request.get_json()
    row = int(data["row"])
    col = int(data["col"])

    if game.is_game_over():
        return jsonify({"error": "Game is already over."}), 400

    print(f"Human attempted move at: ({row}, {col})")

    move_successful = game.make_move(row, col, HUMAN_PLAYER)
    if not move_successful:
        return jsonify({"error": "Invalid move."}), 400

    if not game.is_game_over():
        ai_move = ai.get_best_move(game)
        if ai_move:
            print(f"AI plays at: {ai_move}")
            game.make_move(ai_move[0], ai_move[1], AI_PLAYER)

    response = {
        "board": convert_board_to_json_compatible(game.get_visible_board()),
        "winner": game.winner,
        "turn": game.current_turn,
        "message": f"{game.winner} wins!" if game.winner else ""
    }
    return jsonify(response)

def convert_board_to_json_compatible(board):
    return [[list(cell) if cell else None for cell in row] for row in board]

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

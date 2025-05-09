import random
from ai_player import AIPlayer
from game_engine import DisappearingTicTacToe
from copy import deepcopy

def random_move(game):
    return random.choice(game.get_valid_moves())

def play_game(ai_symbol):
    game = DisappearingTicTacToe()
    ai = AIPlayer(ai_symbol)
    opponent = "O" if ai_symbol == "X" else "X"
    current = "X"

    while not game.is_game_over() and game.get_valid_moves():
        if current == ai.player:
            move = ai.get_best_move(deepcopy(game))
        else:
            move = random_move(game)
        game.make_move(move[0], move[1], current)
        current = opponent if current == ai_symbol else ai_symbol

    return game.winner

def simulate_games(n=1000):
    ai_wins = 0
    random_wins = 0
    draws = 0

    for i in range(n):
        ai_symbol = "X" if i % 2 == 0 else "O"
        winner = play_game(ai_symbol)

        if winner == ai_symbol:
            ai_wins += 1
        elif winner is None:
            draws += 1
        else:
            random_wins += 1

        if (i + 1) % 100 == 0:
            print(f"{i+1} games completed...")

    print(f"AI Wins:      {ai_wins} ({ai_wins / n * 100:.2f}%)")
    print(f"Random Wins:  {random_wins} ({random_wins / n * 100:.2f}%)")
    print(f"Draws:        {draws} ({draws / n * 100:.2f}%)")

simulate_games(1000)

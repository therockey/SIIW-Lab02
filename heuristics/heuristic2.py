# heuristics/heuristic2.py
import gamelib


def evaluate_board(board, player):
    opponent = 'B' if player == 'W' else 'W'
    my_moves = len(gamelib.get_valid_moves(board, player))
    opponent_moves = len(gamelib.get_valid_moves(board, opponent))
    return my_moves - opponent_moves
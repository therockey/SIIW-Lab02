# heuristics/simple_heuristic.py

def evaluate_board(board, player):
    opponent = 'B' if player == 'W' else 'W'
    my_count = sum(row.count(player) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    return my_count - opponent_count

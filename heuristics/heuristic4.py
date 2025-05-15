# heuristics/heuristic4.py

def evaluate_board(board, player):
    rows = len(board)
    cols = len(board[0])
    center_i = rows / 2
    center_j = cols / 2
    score = 0

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == player:
                distance = abs(i - center_i) + abs(j - center_j)
                score -= distance
    return score

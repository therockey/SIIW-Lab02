# heuristics/heuristic3.py

def evaluate_board(board, player):
    opponent = 'B' if player == 'W' else 'W'
    corners = [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]
    score = 0
    for r, c in corners:
        if board[r][c] == player:
            score += 1
        elif board[r][c] == opponent:
            score -= 1
    return score

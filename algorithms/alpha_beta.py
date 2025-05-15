import gamelib


def evaluate(board, depth, is_maximizing, player, heuristic, beta=float('inf'), alpha=float('-inf')):
    opponents = {
        'W': 'B',
        'B': 'W'
    }

    moves = gamelib.get_valid_moves(board, player)
    if depth == 0 or not moves:
        return heuristic.evaluate_board(board, player), None

    best_eval = float('-inf') if is_maximizing else float('inf')
    best_move = None
    for move in gamelib.get_valid_moves(board, player):
        new_board = gamelib.apply_move(board, move, player)
        score, _ = evaluate(new_board, depth - 1, not is_maximizing, opponents[player], heuristic)
        if is_maximizing:
            if score > best_eval:
                best_eval = score
                best_move = move
            alpha = max(alpha, best_eval)
            if beta <= alpha:
                break
        else:
            if score < best_eval:
                best_eval = score
                best_move = move
            beta = min(beta, best_eval)
            if beta <= alpha:
                break
    return best_eval, best_move

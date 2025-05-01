# heuristics/simple_heuristic.py

def get_valid_moves(board, player):
    opponent = 'B' if player == 'W' else 'W'
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    moves = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == player:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                        if board[nr][nc] == opponent:
                            moves.append(((r, c), (nr, nc)))
    return moves

def apply_move(board, move, player):
    from_r, from_c = move[0]
    to_r, to_c = move[1]
    new_board = [row[:] for row in board]
    new_board[to_r][to_c] = player
    new_board[from_r][from_c] = '.'
    return new_board

def evaluate_board(board, my_player):
    opponent = 'B' if my_player == 'W' else 'W'
    my_count = sum(row.count(my_player) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    return my_count - opponent_count

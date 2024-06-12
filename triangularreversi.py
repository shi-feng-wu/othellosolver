# Shi Feng Wu (118335582)
EMPTY = 0
PLAYER = 1
OPPONENT = 2
INVALID = 3
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def get_valid_moves(board, player):
    valid_moves = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell != EMPTY: continue
            for x, y in DIRECTIONS:
                    if is_valid_move(board, i, j, player, x, y):
                        valid_moves.append((i, j))
                        break
    return valid_moves

def is_valid_move(board, row, col, player, x, y):
    rows = len(board)
    row += x
    col += y
    op = OPPONENT if player == PLAYER else PLAYER

    if not (0 <= row < rows and 0 <= col < len(board[row]) and board[row][col] == op):
        return False
    
    row += x
    col += y
    while 0 <= row < rows and 0 <= col < len(board[row]) and board[row][col] is not INVALID:
        if board[row][col] == EMPTY:
            return False
        if board[row][col] == player:
            return True
        row += x
        col += y
    return False

def evaluate_board(board):
    player_score = sum(x.count(PLAYER) for x in board)
    opponent_score = sum(x.count(OPPONENT) for x in board)
    return player_score - opponent_score

def minimax(board, depth, player, alpha, beta, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board), None
    
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return minimax(board, depth - 1, OPPONENT if player == PLAYER else OPPONENT, alpha, beta, not maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves:
            changes = make_move(board, move, player)
            evaluation, _ = minimax(board, depth - 1, OPPONENT, alpha, beta, False)
            undo_move(board, changes)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            if max_eval > beta: break
            alpha = max(alpha, max_eval)  
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for move in valid_moves:
            changes = make_move(board, move, player)
            evaluation, _ = minimax(board, depth - 1, PLAYER, alpha, beta, True)
            undo_move(board, changes)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            if min_eval < alpha: break
            beta = min(beta, min_eval)
        return min_eval, best_move

def make_move(board, move, player):
    row, col = move
    board[row][col] = player
    changes = [(row, col, EMPTY)]
    for x, y in DIRECTIONS:
        row_pos, col_pos = row + x, col + y
        discs_to_flip = []
        while 0 <= row_pos < len(board) and 0 <= col_pos < len(board[0]) and board[row_pos][col_pos] == (OPPONENT if player == PLAYER else PLAYER):
            discs_to_flip.append((row_pos, col_pos))
            row_pos += x
            col_pos += y
            if 0 <= row_pos < len(board) and 0 <= col_pos < len(board[0]) and board[row_pos][col_pos] == player:
                for flip_row, flip_col in discs_to_flip:
                    changes.append((flip_row, flip_col, board[flip_row][flip_col]))
                    board[flip_row][flip_col] = player
                break
    return changes

def undo_move(board, changes):
    for row, col, original in changes:
        board[row][col] = original

def game_over(board):
    a = get_valid_moves(board, PLAYER)
    b = get_valid_moves(board, OPPONENT)
    return not a and not b

import time
def main():
    board = []
    for i in range(10):
        fill = 9 - i
        board.append(([INVALID] * fill) + [int(x) for x in input().split()] + ([INVALID] * fill))
    start_time = time.time()
    best_score, best_move = minimax(board, 5, PLAYER, float('-inf'), float('inf'), True)
    a = best_move[0]
    invalid = int(board[a].count(INVALID) / 2)
    b = best_move[1] - invalid
    print(f"{a + 1} {b + 1}") if best_move else print("")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    
main()
from . import engine
from .constants import WHITE, BLACK


def minimax(board, player, depth, is_max):

    if depth == 0:
        board.ai_calc_score()
        return board

    if is_max:
        max_val = Board()
        max_val.nega_score = -1000
        for move in board.available_moves(player):
            new_board = Board(board, board.white_score,board.black_score).is_valid(move[0], move[1], player)
            eval = minimax(new_board, engine.reverse_player(player), depth - 1, False)
            max_val = max(max_val, eval, lambda x: x.nega_score)
        return max_val
    else:
        min_val = Board()
        min_val.nega_score = 1000
        for move in board.available_moves(player):
            new_board = Board(board, board.white_score, board.black_score).is_valid(move[0], move[1], player)
            eval = minimax(new_board, engine.reverse_player(player), depth - 1, True)
            min_val = min(min_val, eval, lambda x: x.nega_score)
        return min_val


def interface(board, player, depth=4):
    root = deepcopy(board)
    return minimax(root, player, depth, True)


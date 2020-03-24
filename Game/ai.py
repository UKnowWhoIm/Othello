if __name__ == "__main__":
    import engine
    from constants import WHITE, BLACK
else:
    from . import engine
    from .constants import WHITE, BLACK

from copy import deepcopy
from time import time


def minimax(board, player, depth, is_max, alpha=-1000, beta=1000):
    if depth == 0:
        return board.ai_calc_score()
    break_loop = False
    if is_max:
        max_val = -1000
        for i in range(8):
            for j in range(8):
                temp = deepcopy(board)
                if temp.is_valid(i, j, player):
                    val = minimax(temp, engine.reverse_player(player), depth - 1, False)
                    if val > max_val:
                        max_val = val
                    alpha = max(max_val, alpha)
                    if alpha <= beta:
                        break_loop = True
                        break
            if break_loop:
                break
        return max_val

    else:
        min_val = 1000
        for i in range(8):
            for j in range(8):
                temp = deepcopy(board)
                if temp.is_valid(i, j, player):
                    val = minimax(temp, engine.reverse_player(player), depth - 1, True)
                    if val < min_val:
                        min_val = val
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        break_loop = True
                        break
            if break_loop:
                break
        return min_val


"""


def minimax(board, player, depth, is_max):
    if depth == 0:
        return board.ai_calc_score()
    if is_max:
        max_val = -1000
        for move in board.available_moves(player):
            new_board = engine.Board(board.board, board.white_score, board.black_score)
            new_board.is_valid(move[0], move[1], player)
            eval = minimax(new_board, engine.reverse_player(player), depth - 1, False)
            max_val = max(max_val, eval)
        return max_val

    else:
        min_val = 1000
        for move in board.available_moves(player):
            new_board = engine.Board(board.board, board.white_score, board.black_score)
            new_board.is_valid(move[0], move[1], player)
            eval = minimax(new_board, engine.reverse_player(player), depth - 1, True)
            min_val = min(min_val, eval)
        return min_val
"""


def interface(board, player, depth=4):
    max_val = -10000
    coods = (-1, -1)

    for i in range(8):
        for j in range(8):
            temp = deepcopy(board)
            if temp.is_valid(i, j, player):
                val = minimax(temp, engine.reverse_player(player), depth - 1, False)
                print(val)
                if val > max_val:
                    max_val = val
                    coods = (i, j)
    return coods


if __name__ == "__main__":
    """
    board = engine.Board()
    board.is_valid(3, 5, WHITE)
    board.print_board()
    interface(board, BLACK, 4).print_board()
    """
    pass

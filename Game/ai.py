if __name__ == "__main__":
    import engine
    from constants import WHITE, BLACK
else:
    from . import engine
    from .constants import WHITE, BLACK
    from time import time
from copy import deepcopy


def minimax(board, root_player, player, depth, is_max, alpha=-1000, beta=1000):
    if depth == 0:
        return board.ai_calc_score(is_max, player)

    break_loop = False
    if is_max:
        max_val = -1000
        for i in range(8):
            for j in range(8):
                [move_is_valid, flipped_pieces] = board.is_valid(i, j, player, True)
                if move_is_valid:
                    temp = deepcopy(board)
                    temp.flip_pieces(flipped_pieces, player)
                    val = minimax(temp, root_player, engine.reverse_player(player), depth - 1, False)
                    if val > max_val:
                        max_val = val
                    alpha = max(max_val, alpha)
                    if beta <= alpha:
                        # print('prune')
                        break_loop = True
                        break
            if break_loop:
                break
        return alpha

    else:
        min_val = 1000
        for i in range(8):
            for j in range(8):
                [move_is_valid, flipped_pieces] = board.is_valid(i, j, player, True)
                if move_is_valid:
                    temp = deepcopy(board)
                    temp.flip_pieces(flipped_pieces, player)
                    val = minimax(temp, root_player, engine.reverse_player(player), depth - 1, True)
                    if val < min_val:
                        min_val = val
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        # print('prune')
                        break_loop = True
                        break
            if break_loop:
                break
        return beta


def interface(board, player, depth=3):
    a = time()
    coods = (-1, -1)
    initial_moves = []
    for i in range(8):
        for j in range(8):
            [move_is_valid, flipped_pieces] = board.is_valid(i, j, player, True)
            if move_is_valid:
                temp = deepcopy(board)
                temp.flip_pieces(flipped_pieces, player)
                initial_moves.append((temp, [i, j]))

    initial_moves = sorted(initial_moves, key=lambda x:x[0].ai_calc_score(True, player), reverse=True)

    alpha = -10000
    for move in initial_moves:
        temp = move[0]
        [i, j] = move[1]
        val = minimax(temp, player, engine.reverse_player(player), depth - 1, False, alpha)
        if val > alpha:
            alpha = val
            coods = (i, j)

    print(time() - a)
    return coods


if __name__ == "__main__":
    pass

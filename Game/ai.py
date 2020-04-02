if __name__ == "__main__":
    import engine
    from constants import WHITE, BLACK
else:
    from . import engine
    from .constants import WHITE, BLACK

from copy import deepcopy



def minimax(board, root_player, player, depth, is_max, alpha=-1000, beta=1000):
    if depth == 0:
        if root_player == WHITE:
            return board.ai_calc_score() * -1
        return board.ai_calc_score()
    break_loop = False
    if is_max:
        max_val = -1000
        for i in range(8):
            for j in range(8):
                temp = deepcopy(board)
                if temp.is_valid(i, j, player):
                    val = minimax(temp, root_player, engine.reverse_player(player), depth - 1, False)
                    if val > max_val:
                        max_val = val
                    alpha = max(max_val, alpha)
                    if beta <= alpha:
                        print('prune')
                        break_loop = True
                        break
            if break_loop:
                break
        return alpha

    else:
        min_val = 1000
        for i in range(8):
            for j in range(8):
                temp = deepcopy(board)
                if temp.is_valid(i, j, player):
                    val = minimax(temp, root_player, engine.reverse_player(player), depth - 1, True)
                    if val < min_val:
                        min_val = val
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        print('prune')
                        break_loop = True
                        break
            if break_loop:
                break
        return beta


def interface(board, player, depth=4):
    max_val = -10000
    coods = (-1, -1)

    for i in range(8):
        for j in range(8):
            temp = deepcopy(board)
            if temp.is_valid(i, j, player):
                val = minimax(temp, player, engine.reverse_player(player), depth - 1, False)
                # print(val)
                if val > max_val:
                    max_val = val
                    coods = (i, j)
    return coods


if __name__ == "__main__":
    pass

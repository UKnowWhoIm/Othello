from copy import deepcopy
from .constants import WHITE, BLACK
# from constants import WHITE, BLACK
dirns = [[-1, -1], [-1, 1], [-1, 0], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]


class Board:
    def __init__(self, board=None, white_score=None, black_score=None):
        if board:
            self.board = deepcopy(board)
            self.white_score = white_score
            self.black_score = black_score
        else:
            self.board = {(3, 3): WHITE, (3, 4): BLACK, (4, 4): WHITE, (4, 3): BLACK}
            self.white_score = 2
            self.black_score = 2

    def is_valid(self, x, y, player, sim=False):

        if (x, y) == (-1, -1):
            if sim:
                return [self.check_pass(player), []]
            else:
                return self.check_pass(player)
        if self.board.get((x, y), None):
            # Target col is occupied
            if sim:
                return [False,[]]
            return False
        move_is_valid = False
        flipped_pieces = [(x, y)]
        for dirn in dirns:
            new_flipped_pieces = []
            piece_flipped = False
            encountered_self = False
            temp_x, temp_y = x + dirn[0], y + dirn[1]
            while 0 <= temp_x <= 7 and 0 <= temp_y <= 7:
                if self.board.get((temp_x, temp_y), None) == reverse_player(player):
                    piece_flipped = True
                    new_flipped_pieces.append((temp_x, temp_y))
                    temp_x += dirn[0]
                    temp_y += dirn[1]

                elif self.board.get((temp_x, temp_y), None) == player:
                    encountered_self = True
                    break
                else:
                    break
            if piece_flipped and encountered_self:
                # Move is valid as at least one piece is flipped
                move_is_valid = True
                # as this board is valid, append pieces to flipped pieces
                flipped_pieces += new_flipped_pieces

        if move_is_valid and not sim:
            self.flip_pieces(flipped_pieces, player)
            self.calc_score()
        elif sim:
            return [move_is_valid, flipped_pieces]
        return move_is_valid

    def calc_score(self):
        self.white_score = 0
        self.black_score = 0
        for pos, player in self.board.items():
            if player == WHITE:
                self.white_score += 1
            elif player == BLACK:
                self.black_score += 1

    def available_moves(self, player):
        moves = []
        for pos, player_ in self.board.items():
            if player == reverse_player(player_):
                for dirn in dirns:
                    tempx, tempy = pos[0] + dirn[0], pos[1] + dirn[1]
                    if 0 <= tempx <= 7 and 0 <= tempy <= 7:
                        if self.is_valid(pos[0] + dirn[0], pos[1] + dirn[1], player, True)[0]:
                            moves.append((pos[0] + dirn[0], pos[1] + dirn[1]))
        return moves

    def check_pass(self, player):
        # A player passes his turn when there are no available moves
        return not self.available_moves(player)

    def has_game_ended(self):
        return self.check_pass(WHITE) and self.check_pass(BLACK)

    def ai_calc_score(self, ai_player, current_player):
        if ai_player != current_player:
            multiplier = -1
        else:
            multiplier = 1
        score = 0
        if multiplier == 1 and current_player == WHITE or multiplier == -1 and current_player == BLACK:
            # WHITE is maximising
            basic_score = self.white_score - self.black_score
        else:
            # BLACK is maximising
            basic_score = self.black_score - self.white_score

        score += basic_score
        edge_factor = 4
        corner_factor = 8

        for i in range(8):
            for j in range(8):
                if self.board.get((i, j), None):
                    if is_edge(i, j):
                        if is_corner(i, j):
                            if self.board[(i, j)] == current_player:
                                score += corner_factor * 1 * multiplier
                            else:
                                score += corner_factor * -1 * multiplier
                        else:
                            if self.board[(i, j)] == current_player:
                                score += edge_factor * 1 * multiplier
                            else:
                                score += edge_factor * -1 * multiplier
        return score

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board.get((i, j), None):
                    if self.board[(i, j)] == WHITE:
                        print('w', end=' ')
                    else:
                        print('b', end=' ')
                else:
                    print('.', end=' ')
            print()

    def flip_pieces(self, flipped_pieces, player):
        for piece in flipped_pieces:
            self.board[piece] = player

def reverse_player(player):
    if player == BLACK:
        return WHITE
    return BLACK

def is_edge(x, y):
    return x == 0 or x == 7 or y == 0 or y == 7

def is_corner(x, y):
    return (x == 0 or x == 7) and (y == 0 or y == 7)

if __name__ == '__main__':
    pass

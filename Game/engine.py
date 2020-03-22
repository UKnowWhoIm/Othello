from copy import deepcopy
from .constants import WHITE, BLACK
dirns = [[-1, -1], [-1, 1], [-1, 0], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]


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
        self.nega_score = 0

    def is_valid(self, x, y, player, sim=False):
        if (x, y) == (-1, -1):
            return self.check_pass(player)
        if self.board.get((x, y), None):
            # Target col is occupied
            return False

        move_is_valid = False
        for dirn in dirns:
            temp_board = Board(self.board, self.white_score, self.black_score).board
            piece_flipped = False
            encountered_self = False
            temp_x, temp_y = x + dirn[0], y + dirn[1]
            while 0 <= temp_x <= 7 and 0 <= temp_y <= 7:
                if temp_board.get((temp_x, temp_y), None) == reverse_player(player):
                    piece_flipped = True
                    temp_board[(temp_x, temp_y)] = player
                    temp_x += dirn[0]
                    temp_y += dirn[1]
                elif temp_board.get((temp_x, temp_y), None) == player:
                    encountered_self = True
                    break
                else:
                    break
            if piece_flipped and encountered_self:
                # Move is valid as at least one piece is flipped
                move_is_valid = True
                self.board = deepcopy(temp_board)
        if move_is_valid and not sim:
            self.board[(x, y)] = player
            self.calc_score()
        elif sim:
            return move_is_valid
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
                    if self.is_valid(pos[0] + dirn[0], pos[1] + dirn[1], player, True):
                        moves.append((pos[0] + dirn[0], pos[1] + dirn[1]))
        return moves

    def check_pass(self, player):
        # A player passes his turn when there are no available moves
        return not self.available_moves(player)

    def has_game_ended(self):
        return self.check_pass(WHITE) and self.check_pass(BLACK)

    def ai_calc_score(self):
        self.nega_score = self.black_score - self.white_score


def reverse_player(player):
    if player == WHITE:
        return BLACK
    return WHITE



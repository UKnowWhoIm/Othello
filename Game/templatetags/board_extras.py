from django import template

register = template.Library()


@register.filter
def convert_board(dic_board):
    list_board = []
    for i in range(8):
        for j in range(8):
            list_board[i][j] = dic_board.get((i, j), None)
    return list_board


@register.filter
def process_game_data(game_over, player):
    if game_over:
        return player + " Has Won"
    return player + "\'s Turn"

from django import template

register = template.Library()


@register.filter
def convert_board(dic_board):
    list_board = [[None for i in range(8)] for j in range(8)]
    for pos, player in dic_board.items():
        list_board[pos[0]][pos[1]] = player
    return list_board


@register.filter
def process_game_data(game_over, player):
    if game_over:
        return player + " Has Won"
    return player + "\'s Turn"

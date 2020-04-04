from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import engine
from .constants import *
from . import ai
import random


def check_game_over(request):
    if request.session['board'].has_game_ended():
        request.session['game_over'] = True
        if request.session['board'].white_score > request.session['board'].black_score:
            request.session['player'] = WHITE
        elif request.session['board'].white_score < request.session['board'].black_score:
            request.session['player'] = BLACK
        else:
            request.session['player'] = None
        return True
    return False


def process_move(request):
    x = int(request.POST['targetX'])
    y = int(request.POST['targetY'])
    if request.session['board'].is_valid(x, y, request.session['player']):
        if [x, y] == [-1, -1]:
            if check_game_over(request):
                return HttpResponse(SUCCESS_CODE)
        request.session['player'] = engine.reverse_player(request.session['player'])
        return HttpResponse(SUCCESS_CODE)
    return HttpResponse(FAILURE_CODE)


def minimax_move(request, depth):
    move = ai.interface(request.session['board'], request.session['player'], depth)

    request.session['board'].is_valid(move[0], move[1], request.session['player'])
    if move == (-1, -1):
        if check_game_over(request):
            return HttpResponse(SUCCESS_CODE)
    request.session['player'] = engine.reverse_player(request.session['player'])
    return HttpResponse(SUCCESS_CODE)


def random_move(request):
    moves = request.session['board'].available_moves(request.session['player'])
    if moves:
        move = random.choice(moves)
        request.session['board'].is_valid(move[0], move[1], request.session['player'])
    else:
        if check_game_over(request):
            return HttpResponse(SUCCESS_CODE)
    request.session['player'] = engine.reverse_player(request.session['player'])
    return HttpResponse(SUCCESS_CODE)


def index_view(request):
    if request.session.get('board', None) is None:
        request.session['board'] = engine.Board()
        request.session['player'] = WHITE
        request.session['game_over'] = False
    return render(request, "reversi/game.html")


def new_game(request):
    request.session.flush()
    request.session['ai_disabled'] = False
    request.session['player_disabled'] = False
    if int(request.GET['mode']) == 1:
        # Quick Match
        request.session['ai_color'] = BLACK
        request.session['black_type'] = 1
        request.session['black_depth'] = 4

    elif int(request.GET['mode']) == 2:
        # Custom Match
        request.session['black_type'] = int(request.GET['type'])
        if request.session['black_type'] == 1:
            if 1 <= int(request.GET['depth']) <= 7:
                request.session['black_depth'] = int(request.GET['depth'])
            else:
                request.session['black_depth'] = 4

    elif int(request.GET['mode']) == 3:
        # Multi player
        request.session['ai_disabled'] = True

    else:
        # AI v AI
        request.session['white_type'] = int(request.GET['white_type'])
        request.session['black_type'] = int(request.GET['black_type'])
        if request.session['white_type'] == 1:
            # Minimax with alpha beta pruning
            request.session['white_depth'] = int(request.GET['white_depth'])
        if request.session['black_type'] == 1:
            # Minimax with alpha beta pruning
            request.session['black_depth'] = int(request.GET['black_depth'])

        request.session['player_disabled'] = True

    return HttpResponseRedirect('/reversi')


def landing(request):
    return render(request, "reversi/landing.html")


def ai_move_handler(request):
    if request.session['player'] == WHITE:
        if request.session.get('white_type', None) is None:
            return HttpResponse(FAILURE_CODE)
        type = 'white_type'
        depth = 'white_depth'
    else:
        type = 'black_type'
        depth = 'black_depth'
    if request.session[type] == 1:
        # Minimax with alpha beta pruning
        minimax_move(request, request.session[depth])
    elif request.session[type] == 2:
        # Random Move
        random_move(request)
    else:
        # Greedy Move
        minimax_move(request, 1)
    return HttpResponse(SUCCESS_CODE)

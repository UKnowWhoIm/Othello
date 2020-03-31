from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import engine
from .constants import *
from . import ai


def process_move(request):
    x = int(request.POST['targetX'])
    y = int(request.POST['targetY'])
    if request.session['board'].is_valid(x, y, request.session['player']):
        if [x, y] == [-1, -1]:
            if request.session['board'].has_game_ended():
                request.session['game_over'] = True
                if request.session['board'].white_score > request.session['board'].black_score:
                    request.session['player'] = WHITE
                elif request.session['board'].white_score < request.session['board'].black_score:
                    request.session['player'] = BLACK
                else:
                    request.session['player'] = None
                return HttpResponse(SUCCESS_CODE)
        request.session['player'] = engine.reverse_player(request.session['player'])
        return HttpResponse(SUCCESS_CODE)
    return HttpResponse(FAILURE_CODE)


def ai_move(request):
    move = ai.interface(request.session['board'], request.session['player'], request.session['depth'])
    request.session['board'].is_valid(move[0], move[1], request.session['player'])
    if move == (-1, -1):
        if request.session['board'].has_game_ended():
            request.session['game_over'] = True
            if request.session['board'].white_score > request.session['board'].black_score:
                request.session['player'] = WHITE
            elif request.session['board'].white_score < request.session['board'].black_score:
                request.session['player'] = BLACK
            else:
                request.session['player'] = None
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
        request.session['depth'] = 3
        request.session['ai_color'] = BLACK
    elif int(request.GET['mode']) == 2:
        # Custom Match
        request.session['depth'] = int(request.GET['depth'])
        print(request.GET['color'], engine.reverse_player(request.GET['color']))
        request.session['ai_color'] = engine.reverse_player(request.GET['color'])
    elif int(request.GET['mode']) == 3:
        # Multi player
        request.session['ai_disabled'] = True
    else:
        # AI v AI
        request.session['depth'] = int(request.GET['depth'])
        request.session['player_disabled'] = True
    return HttpResponseRedirect('/reversi')


def landing(request):
    return render(request, "reversi/landing.html")

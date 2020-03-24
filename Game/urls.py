from . import views
from django.urls import path

urlpatterns = [
    path('process_move', views.process_move, name="Move"),
    path('', views.index_view, name='Home'),
    path('new_game', views.new_game, name='new_game'),
    path('ai_move', views.ai_move, name='ai_move'),
]

from django.urls import path
from .views import play_game, view_scoreboard

app_name = 'game'

urlpatterns = [
    path('play/', play_game, name='play_game'),
    path('scoreboard/', view_scoreboard, name='view_scoreboard'),
]

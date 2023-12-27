from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('game/joingame/', views.JoinGame.as_view()),
    path('game/playround/', views.PlayRound.as_view()),
    path('game/getscore/', views.UpdateScore.as_view()),
    path('game/scoreboard/', views.ViewScoreboard.as_view()),
]

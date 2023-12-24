# game/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GameRound
from .serializers import GameRoundSerializer
import random


class PlayGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        rounds_to_win = 3
        player_wins = 0
        opponent_wins = 0
        rounds_played = 0

        player_choice = request.data.get('choice')
        opponent_choice = random.choice(['rock', 'paper', 'scissors'])

        result = self.determine_result(player_choice, opponent_choice)

        rounds_played += 1
        if result == 'win':
            player_wins += 1
        elif result == 'lose':
            opponent_wins += 1

        GameRound.objects.create(
            player=request.user,
            opponent=opponent_choice,
            result=result
        )

        if player_wins == rounds_to_win or opponent_wins == rounds_to_win:
            if player_wins > opponent_wins:
                request.user.userprofile.score += 3
            elif player_wins < opponent_wins:
                request.user.userprofile.score -= 1
            request.user.userprofile.save()

            return Response({'detail': 'Game over', 'scoreboard_url': 'game:view_scoreboard'}, status=status.HTTP_200_OK)

        return Response({
            'rounds_played': rounds_played,
            'player_wins': player_wins,
            'opponent_wins': opponent_wins,
        }, status=status.HTTP_200_OK)

    def determine_result(self, player_choice, opponent_choice):
        if player_choice == opponent_choice:
            return 'tie'
        elif (
            (player_choice == 'rock' and opponent_choice == 'scissors') or
            (player_choice == 'paper' and opponent_choice == 'rock') or
            (player_choice == 'scissors' and opponent_choice == 'paper')
        ):
            return 'win'
        else:
            return 'lose'


class ViewScoreboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        game_rounds = GameRound.objects.filter(player=request.user)
        serializer = GameRoundSerializer(game_rounds, many=True)
        return Response({'game_rounds': serializer.data}, status=status.HTTP_200_OK)

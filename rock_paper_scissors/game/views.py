# game/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializer
from user import models as UserModel
import random


class JoinGame(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        objs = models.Competition.objects.filter(complete=False).\
            exclude(id__in=models.Participation.objects.filter(player=request.user).values('competition'))\
            .order_by('create_date')

        if len(objs) > 0:
            competition = objs.first()
            competition.complete = True
            competition.save()
        else:
            competition = models.Competition()
            competition.save()

        data = {
            "player": request.user.id,
            "competition": competition.id
        }
        s = serializer.JoinGameSerializer(data=data)
        if s.is_valid():
            s.save()
            response = {
                "status": 200,
                "message": "game joined or created successfully"
            }
            return Response(response, status.HTTP_200_OK)
        response = {
            "status": 400,
            "message": 'invalid request'
        }
        return Response(s.errors, status.HTTP_400_BAD_REQUEST)


class PlayRound(APIView):
    def post(self, request):
        cid = request.data["cid"]
        participation = models.Participation.objects.filter(player=request.user, competition_id=cid).first()
        if participation is None:
            response = {
                "status": 404,
                "message": "competition not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        currentRound = request.data['whichRound']
        player_choice = request.data['choice']

        data = {
            "whichRound": currentRound,
            "player": request.user.id,
            "competition": cid,
            "choice": player_choice,
        }
        s = serializer.GameRoundSerializer(data=data)
        if s.is_valid():
            s.save()
            response = {
                "status": 200,
                "message": 'round player successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": 404,
            "message": "invalid request"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UpdateScore(APIView):
    def post(self, request):
        cid = request.data["cid"]
        firstGameRoundForUser = models.GameRound.objects.filter(player=request.user, competition__id=cid, whichRound="one").first()
        firstGameRoundForOpponent = models.GameRound.objects.filter(competition__id=cid, whichRound="one").exclude(player=request.user).first()
        secondGameRoundForUser = models.GameRound.objects.filter(player=request.user, competition__id=cid, whichRound="two").first()
        secondGameRoundForOpponent = models.GameRound.objects.filter(competition__id=cid, whichRound="two").exclude(player=request.user).first()
        thirdGameRoundForUser = models.GameRound.objects.filter(player=request.user, competition__id=cid, whichRound="three").first()
        thirdGameRoundForOpponent = models.GameRound.objects.filter(competition__id=cid, whichRound="three").exclude(player=request.user).first()

        if firstGameRoundForUser is None or firstGameRoundForOpponent is None or secondGameRoundForUser is None or secondGameRoundForOpponent is None or thirdGameRoundForUser is None or thirdGameRoundForOpponent is None:
            response = {
                "status": 404,
                "message": "competition not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        first_user_choice = firstGameRoundForUser.choice
        first_opponent_choice = firstGameRoundForOpponent.choice
        first_result = self.determine_result(first_user_choice, first_opponent_choice)

        second_user_choice = secondGameRoundForUser.choice
        second_opponent_choice = secondGameRoundForOpponent.choice
        second_result = self.determine_result(second_user_choice, second_opponent_choice)

        third_user_choice = thirdGameRoundForUser.choice
        third_opponent_choice = thirdGameRoundForOpponent.choice
        third_result = self.determine_result(third_user_choice, third_opponent_choice)

        user_wins = 0
        opponent_wins = 0

        if first_result == 'win':
            user_wins += 1
        elif first_result == 'lose':
            opponent_wins += 1

        if second_result == 'win':
            user_wins += 1
        elif second_result == 'lose':
            opponent_wins += 1

        if third_result == 'win':
            user_wins += 1
        elif third_result == 'lose':
            opponent_wins += 1

        user_score = 0
        opponent_score = 0

        if user_wins == opponent_wins:
            user_score = 1
            opponent_score = 1
        elif user_wins > opponent_wins:
            user_score = 3
        else:
            opponent_score = 3

        print(user_score, opponent_score)

        user = UserModel.User.objects.filter(username=request.user.username).first()
        user.score += user_score
        user.save()

        opponent = UserModel.User.objects.filter(username=firstGameRoundForOpponent.player.username).first()
        opponent.score += opponent_score
        opponent.save()

        response = {
            "status": 200,
            "message": "score updated successfully"
        }
        return Response(response, status=status.HTTP_200_OK)
        # opponentProfile = models.UserProfile.objects.filter(user__id=firstGameRoundForOpponent.player.id)
        # opponentProfile.score += opponent_score
        # opponentProfile.save()




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

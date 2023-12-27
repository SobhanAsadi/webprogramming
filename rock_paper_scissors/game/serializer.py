from rest_framework import serializers
from . import models


class GameRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameRound
        fields = '__all__'


class JoinGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = '__all__'

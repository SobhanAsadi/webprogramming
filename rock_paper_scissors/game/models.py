from django.db import models
from django.contrib.auth import get_user_model


class GameRound(models.Model):
    player = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    opponent = models.CharField(max_length=255)
    result = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

from django.db import models
from user import models as UserModel
from django.utils import timezone


class Competition(models.Model):
    create_date = models.DateTimeField(default=timezone.localtime, blank=True)
    complete = models.BooleanField(default=False)


class Participation(models.Model):
    player = models.ForeignKey(UserModel.User, on_delete=models.DO_NOTHING, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(default=timezone.localtime, blank=True)


class GameRound(models.Model):
    whichRound = models.CharField(max_length=255, choices={('one', 'one'), ('two', 'two'), ('three', 'three')}, default='one')
    player = models.ForeignKey(UserModel.User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING, null=True)
    choice = models.CharField(max_length=255, choices=[('rock', 'rock'), ('paper', 'paper'), ('scissors', 'scissors')], default='rock')
    timestamp = models.DateTimeField(default=timezone.localtime, blank=True)

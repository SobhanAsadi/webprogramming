from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=255)
    nicknameColor = models.CharField(max_length=255, default='black')  # add desired colors as choices
    score = models.IntegerField(default=0)

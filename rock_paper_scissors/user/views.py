from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token as RestToken
from rest_framework import status

from . import models


class Users(APIView):

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        nickname = request.data["nickname"]

        user = models.User.objects.create_user(username=username, password=password, nickname=nickname,
                                               nicknameColor='black', is_staff=False)
        token, created = RestToken.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)

    def get(self, request):
        pass

    def delete(self, request):
        pass

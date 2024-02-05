from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token as RestToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from . import serializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError


class SignupUser(APIView):
    permission_classes = ()

    def post(self, request):
        se = serializer.NormalUserSerializer(data=request.data)
        if se.is_valid():
            se.save()
            response = {
                'status': 201,
                'message': "User registered successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            errorMessage = ""
            errors = list(se.errors.items())
            error = errors[0]
            if error[1][0] == "This field may not be blank.":
                errorMessage = f"{error[0]} must not be blank."
            else:
                errorMessage = error[1][0]
            response = {
                'status': 400,
                'message': errorMessage
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = ()

    def post(self, request):
        data = {
            "username": request.data["username"],
            "password": request.data["password"]
        }
        se = AuthTokenSerializer(data=data, context={"request": request})
        try:
            se.is_valid(raise_exception=True)
        except AuthenticationFailed:
            response = {
                "status": 401,
                "message": "Authentication failed",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError:
            response = {
                "status": 400,
                "message": "invalid username or password"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            errorMessage = list(se.errors.values())[0][0]
            response = {
                "status": 400,
                "message": errorMessage
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user = se.validated_data['user']
        if user.is_staff:
            response = {
                "status": 403,
                "message": "Staff users cannot login as normal users"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        token, created = RestToken.objects.get_or_create(user=user)
        response = {
            "status": 200,
            "message": "User logged in successfully",
            "data": {
                "Token": token.key
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class SignupStaffUser(APIView):
    permission_classes = ()

    def post(self, request):
        se = serializer.StaffUserSerializer(data=request.data)
        if se.is_valid():
            se.save()
            response = {
                'status': 201,
                'message': "Staff registered successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            errorMessage = ""
            errors = list(se.errors.items())
            error = errors[0]
            if error[1][0] == "This field may not be blank.":
                errorMessage = f"{error[0]} must not be blank."
            else:
                errorMessage = error[1][0]
            response = {
                'status': 400,
                'message': errorMessage
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)


class LoginStaffUser(APIView):
    permission_classes = ()

    def post(self, request):
        se = AuthTokenSerializer(data=request.data)
        try:
            se.is_valid(raise_exception=True)
        except AuthenticationFailed:
            response = {
                "status": 401,
                "message": "Invalid username or password",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError:
            response = {
                "status": 400,
                "message": "Invalid username or password"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            errorMessage = list(se.errors.values())[0][0]
            response = {
                "status": 400,
                "message": errorMessage
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user = se.validated_data['user']
        if not user.is_staff:
            response = {
                "status": 403,
                "message": "normal users can't login as staff users"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        token, created = RestToken.objects.get_or_create(user=user)
        response = {
            "status": 200,
            "message": "Staff user logged in successfully",
            "data": {
                "Token": token.key
            }
        }
        return Response(response, status=status.HTTP_200_OK)

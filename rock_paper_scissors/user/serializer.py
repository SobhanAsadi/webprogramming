from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from . import models
from rest_framework.authtoken.models import Token as RestToken


def hasUpperCase(x):
    for i in x:
        if str(i).isupper():
            return True
    return False


def hasLowerCase(x):
    for i in x:
        if str(i).islower():
            return True
    return False


def hasSpecialCharacter(value):
    specialCharacters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    for c in specialCharacters:
        if c in str(value):
            return True
    return False


class NormalUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        RestToken.objects.create(user=user)
        return user

    def validate_username(self, value):
        if len(value) == 0:
            raise ValidationError("Username cannot be blank")
        if len(value) < 6:
            raise ValidationError("Username should be at least 6 characters")
        elif len(value) > 16:
            raise ValidationError("Username should be at most 16 characters")
        elif not str(value).isalnum():
            raise ValidationError("Username characters should be alphanumeric")
        elif models.User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password should be at least 8 characters")
        elif len(value) > 32:
            raise ValidationError("Password should be at most 32 characters")
        elif not hasUpperCase(value):
            raise ValidationError("Password should contain at least one upper letter")
        elif not hasLowerCase(value):
            raise ValidationError("Password should contain at least one lower letter")
        elif not hasSpecialCharacter(value):
            raise ValidationError("Password should contain at least one special letter like !@#$%^&*()")
        return value


class StaffUserSerializer(NormalUserSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        RestToken.objects.create(user=user)
        return user

    def validate_username(self, value):
        value = super().validate_username(value)
        return value

    def validate_password(self, value):
        value = super().validate_password(value)
        return value

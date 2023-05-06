from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        lookup_field = 'username'

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Chosen username is not allowed')
        return super().validate(data)


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Chosen username is not allowed')
        return super().validate(data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        if 'confirmation_code' not in self.initial_data:
            raise ValidationError('Field confirmation_code is required')
        code = self.initial_data['confirmation_code']
        username = self.initial_data['username']
        user = get_object_or_404(User, username=username)
        if not user:
            raise ValidationError('User does not exist')
        if not default_token_generator.check_token(user, str(code)):
            raise ValidationError('Confirmation code is incorrect')
        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token)
        }

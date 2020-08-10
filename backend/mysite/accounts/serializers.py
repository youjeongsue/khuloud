from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

# 접속 유지 확인 및 사용자 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 회원가입
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password']
        )
        return user


# 로그인 (커스터마이징 => Serializer)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print('validate data',data)
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.validationError('Unable to log in with provided credentials.')
from cloud.s3_function import *
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from accounts.serializers import (
    UserSerializer,
    LoginSerializer,
    SignUpSerializer,
)
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

# LoadUserAPI
# ssr user loading
# used for read_only endpoints to represent a single model instance.
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        print('Load Me 인증 성공', self.request.user)
        user = UserSerializer(self.request.user).data
        settings.AWS_STORAGE_BUCKET_NAME = user['username']
        return self.request.user

# SignUpAPI
# 회원가입 API
class SignUpAPI(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user.username)
        create_bucket(user.username)
        settings.AWS_STORAGE_BUCKET_NAME=user.username
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(
                user, context = self.get_serializer_context()
            ).data,
            'token': token.key
        })


# LoginAPI: req.data(username, password)=>deserializer=>valid(authenticate)=>serializer
# 로그인 API
class LoginAPI(generics.GenericAPIView):
    # field : username, password
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print('login request가 들어왔으면 말좀 해줘', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data # complex type data
        token, created = Token.objects.get_or_create(user=user)
        print(user, token)
        settings.AWS_STORAGE_BUCKET_NAME=user.username
        return Response({
            'user': UserSerializer(
                user, context = self.get_serializer_context()
            ).data,
            'token': token.key
        })




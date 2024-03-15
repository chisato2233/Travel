# Django imports
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# DRF imports
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# JWT and authentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local imports from serializers module
from .serializers import UserRegistrationSerializer, UserUpdateSerializer


class UserRegistrationView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(serializer.validated_data['password']))
            return Response({"message": "User successfully registered.", "userId": serializer.instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(APIView):
    permission_classes = []  # 允许未认证的用户访问

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 用户验证成功，创建并返回token
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            # 用户验证失败
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)




class GetUserView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 从认证信息中获取用户
        user = request.user
        if user and not user.is_anonymous:
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Token is invalid or expired."}, status=status.HTTP_401_UNAUTHORIZED)




class UpdateUserView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User information successfully updated."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # 假设使用Refresh Token; 获取并尝试黑名单当前Refresh Token
            refresh_token = request.data.get("refresh", None)
            if refresh_token is not None:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # 让前端删除Token
            return Response({"message": "User successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Unauthorized or invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

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

from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer  # 确保从正确的位置导入序列化器

class UserRegistrationView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User successfully registered.",
                "userId": user.id  # 直接从创建的用户对象获取ID
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = []  # 允许未认证的用户访问

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        print(username)
        print(password)
        user = authenticate(request,username=username, password=password)
        

        # 为了调试目的，查找或创建一个用户
        # user, created = User.objects.get_or_create(username=username, defaults={'password': 'password'})
        
        # 由于密码不重要（因为我们不进行验证），你可以选择设置一个默认密码
        # 注意: 实际生产环境中不应该这样做

        # 用户"验证"成功（实际上没有验证），创建并返回token
        print(user)

        
        if user is not None:

            # 用户验证成功，创建并返回token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
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
        print("get")
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
        

'''
curl -X POST http://127.0.0.1:8000/api/diaries/create/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODc3NDMxLCJpYXQiOjE3MTY4NzcxMzEsImp0aSI6IjZkYjkyYmNkYTJiODQyZmRhZjgzYzE5OThkZTI1NDE1IiwidXNlcl9pZCI6MTN9.9mcq_KFxhVXgy0Ta1_PI8RY2NjV8chQw5GbAhHm62-0
" -H "Content-Type: application/json" -d '{
{
  "userId":"13"
  "title": "My Travel Diary",
  "content": "Today, I visited...",
  "date": "2023-07-21",
  "location": "LocationA"
}'

'''
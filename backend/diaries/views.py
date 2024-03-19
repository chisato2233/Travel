from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer
# 假设 huff_compress 和 huff_decompress 位于 compress.py 文件中
from compress import huff_compress, huff_decompress

class DiaryCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 确保用户已认证

    def post(self, request, *args, **kwargs):
        serializer = DiaryEntrySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Diary created successfully.",
                "diary": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "error": "Missing or invalid diary information."
        }, status=status.HTTP_400_BAD_REQUEST)

class UserDiaries(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_diaries = DiaryEntry.objects.filter(user=request.user)
        serializer = DiaryEntrySerializer(user_diaries, many=True)
        return Response(serializer.data)

class DiaryUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, diaryId, *args, **kwargs):
        diary = get_object_or_404(DiaryEntry, id=diaryId)

        if diary.user != request.user:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = DiaryEntrySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Diary updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Missing or invalid update information."}, status=status.HTTP_400_BAD_REQUEST)

class DiaryDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, diaryId, *args, **kwargs):
        diary = get_object_or_404(DiaryEntry, id=diaryId)

        if diary.user != request.user:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        diary.delete()
        return Response({"message": "Diary deleted successfully."}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer
from django.shortcuts import get_object_or_404

class DiaryCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DiaryEntrySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            diary_entry = serializer.save(user=request.user)
            return Response({
                "message": "Diary created successfully.",
                "diary": DiaryEntrySerializer(diary_entry, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "error": "Missing or invalid diary information."
        }, status=status.HTTP_400_BAD_REQUEST)

class DiaryUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, diaryId, *args, **kwargs):
        diary = get_object_or_404(DiaryEntry, id=diaryId)

        if diary.user != request.user:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = DiaryEntrySerializer(diary, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            diary_entry = serializer.save()
            return Response({
                "message": "Diary updated successfully.",
                "diary": DiaryEntrySerializer(diary_entry, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Missing or invalid update information."
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDiaries(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_diaries = DiaryEntry.objects.filter(user=request.user)
        serialized_diaries = [DiaryEntrySerializer(diary, context={'request': request}).data for diary in user_diaries]
        return Response(serialized_diaries, status=status.HTTP_200_OK)

class DiaryDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, diaryId, *args, **kwargs):
        diary = get_object_or_404(DiaryEntry, id=diaryId)

        if diary.user != request.user:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        diary.delete()
        return Response({"message": "Diary deleted successfully."}, status=status.HTTP_200_OK)

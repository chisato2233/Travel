from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics
from .models import DiaryEntry,DiaryRating
from .serializers import DiaryEntrySerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db import models

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
        
        for diary in serialized_diaries:
            user_rating = DiaryRating.objects.filter(user=request.user, diary_entry_id=diary['id']).first()
            diary['userRating'] = user_rating.rating if user_rating else 0  # 默认返回0表示没有评分
        
        return Response(serialized_diaries, status=status.HTTP_200_OK)
    
class DiaryDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, diaryId, *args, **kwargs):
        diary = get_object_or_404(DiaryEntry, id=diaryId)

        if diary.user != request.user:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        diary.delete()
        return Response({"message": "Diary deleted successfully."}, status=status.HTTP_200_OK)

class GetAllDiariesView(generics.ListAPIView):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    

class RateDiary(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        diary_id = request.data.get('id')
        my_rating = request.data.get('my_rating')

        if my_rating not in [1, 0,-1]:
            return Response({"error": "Invalid rating value. Must be 1 or -1."}, status=status.HTTP_400_BAD_REQUEST)

        diary = get_object_or_404(DiaryEntry, id=diary_id)
        user = request.user

        # Update or create the rating
        rating, created = DiaryRating.objects.update_or_create(
            user=user, diary_entry=diary,
            defaults={'rating': my_rating}
        )

        # Update the total rating
        diary.rating = DiaryRating.objects.filter(diary_entry=diary).aggregate(total=models.Sum('rating'))['total']
        diary.save()

        serialized_diary = DiaryEntrySerializer(diary, context={'request': request}).data
        return Response(serialized_diary, status=status.HTTP_200_OK)
    


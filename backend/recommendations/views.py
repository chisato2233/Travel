# recommendations/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserSearchHistory
from .utils import recommend_attractions
from backend.models import Attraction
import random

class DestinationRecommendationView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

        search_history = UserSearchHistory.objects.filter(user=request.user).order_by('-search_time')

        unique_attractions = list(set([entry.attraction for entry in search_history]))
        random_history_samples = random.sample(unique_attractions, min(5, len(unique_attractions)))

        recommendations = []
        if random_history_samples:
            for attraction in random_history_samples:
                recommendations.extend(recommend_attractions(attraction.id))
        
        recommendations = list({rec.id: rec for rec in recommendations}.values())
        if len(recommendations) < 10:
            additional_attractions = Attraction.objects.exclude(id__in=[rec.id for rec in recommendations]).order_by('?')[:10 - len(recommendations)]
            recommendations.extend(additional_attractions)
        else:
            recommendations = random.sample(recommendations, 10)

        results = []
        for attraction in recommendations:
            results.append({
                "id": attraction.id,
                "name": attraction.name,
                "description": attraction.description,
                "rating": attraction.rating,
                "popularity": attraction.popularity.view_count if hasattr(attraction, 'popularity') else 0,
            })

        return Response(results, status=status.HTTP_200_OK)



import heapq
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.diaries.models import DiaryEntry,DiaryRating
from rest_framework.permissions import IsAuthenticated
from backend.diaries.serializers import DiaryEntrySerializer
class DiaryRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 获取所有日记
        diaries = DiaryEntry.objects.all()

        # 将日记转换为字典列表
        diary_list = []
        for diary in diaries:
            user_rating = DiaryRating.objects.filter(user=request.user, diary_entry_id=diary.id).first()
            diary_list.append({
                "id": diary.id,
                "title": diary.title,
                "content": diary.content,
                "date": diary.date,
                "location": diary.location,
                "author": diary.user.username,
                "rating": diary.rating if hasattr(diary, 'rating') else 0,
                "userRating": user_rating.rating if user_rating else 0
            })

                # 使用大顶堆获取评分最高的前十个日记
        top_diaries = heapq.nlargest(10, diary_list, key=lambda x: x['rating'])

        return Response(top_diaries, status=status.HTTP_200_OK)

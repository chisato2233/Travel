# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from backend.models import Attraction
from backend.diaries.models import DiaryEntry
from backend.diaries.serializers import DiaryEntrySerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse

class AttractionSearchView(APIView):
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', None)
        category = request.GET.get('category', None)
        keywords = request.GET.get('keywords', None)
        rating = request.GET.get('rating', None)
        popularity = request.GET.get('popularity', None)

        if not name:
            return Response({"error": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        attractions = Attraction.objects.all()
        
        results = []
        for attraction in attractions:
            if name.lower() in attraction.name.lower():
                if category and category.lower() not in attraction.category.lower():
                    continue
                if keywords and keywords.lower() not in attraction.description.lower():
                    continue
                if rating and attraction.rating < float(rating):
                    continue
                if popularity and attraction.sales < int(popularity):
                    continue
                results.append({
                    "id": attraction.id,
                    "name": attraction.name,
                    "category": attraction.category,
                    "rating": attraction.rating,
                    "popularity": attraction.sales,
                    "description": attraction.description,
                    "location": attraction.province_city_district,
                    "view_count": attraction.view_count,
                    "images": []  # 假设你有一张存储图片链接的表
                })

                attraction.view_count += 1
                attraction.save()

        if not results:
            return Response({"error": "No attractions found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"attractions": results}, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_diaries(request):
    keywords = request.GET.get('keywords', '')
    user_id = request.GET.get('userId')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    diaries = DiaryEntry.objects.all()
    
    results = []
    for diary in diaries:
        if user_id and diary.user_id != int(user_id):
            continue
        if start_date and diary.date < start_date:
            continue
        if end_date and diary.date > end_date:
            continue
        if keywords and (keywords.lower() not in diary.content.lower() and keywords.lower() not in diary.title.lower()):
            continue
        results.append({
            'id': diary.id,
            'title': diary.title,
            'summary': diary.content[:100],
            'date': diary.date,
            'userId': diary.user_id,
            'username': diary.user.username,
            'images': []  # 假设你有一张存储图片链接的表
        })

    return JsonResponse({'diaries': results}, safe=False)

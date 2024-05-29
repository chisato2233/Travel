from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from backend.models import Attraction
class AttractionSearchView(APIView):
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', None)
        category = request.GET.get('category', None)
        keywords = request.GET.get('keywords', None)
        rating = request.GET.get('rating', None)
        popularity = request.GET.get('popularity', None)

        if not name:
            return Response({"error": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 查询条件
        filters = Q(name__icontains=name)
        if category:
            filters &= Q(category__icontains=category)
        if keywords:
            filters &= Q(description__icontains=keywords)
        if rating:
            filters &= Q(rating__gte=rating)
        if popularity:
            filters &= Q(sales__gte=popularity)
        
        attractions = Attraction.objects.filter(filters)

        if not attractions.exists():
            return Response({"error": "No attractions found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

        results = []
        for attraction in attractions:
            results.append({
                "id": attraction.id,
                "name": attraction.name,
                "category": category,
                "rating": attraction.rating,
                "popularity": attraction.sales,
                "description": attraction.description,
                "location": attraction.province_city_district,
                "images": []  # 假设你有一张存储图片链接的表
            })

        return Response({"attractions": results}, status=status.HTTP_200_OK)

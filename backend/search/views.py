# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import Attraction;
from backend.recommendations.models import AttractionPopularity,UserSearchHistory
from django.db.models import Q
from backend.diaries.models import DiaryEntry
from backend.diaries.serializers import DiaryEntrySerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import random
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# views.py
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import Attraction
from backend.recommendations.models import AttractionPopularity, UserSearchHistory
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
import random

class AttractionSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', None)
        category = request.GET.get('category', None)
        rating = request.GET.get('rating', None)
        popularity = request.GET.get('popularity', None)

        if not name:
            return Response({"error": "Invalid query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        attractions = Attraction.objects.all()

        if rating:
            attractions = attractions.filter(rating__gte=rating)
        if popularity:
            attractions = attractions.filter(popularity__view_count__gte=popularity)

        results = []
        for attraction in attractions:
            if name.lower() in attraction.name.lower():
                # 获取或创建 AttractionPopularity 对象
                attraction_popularity, created = AttractionPopularity.objects.get_or_create(
                    attraction=attraction,
                    defaults={'view_count': random.randint(1, 100)}
                )
                if not created:
                    attraction_popularity.view_count = F('view_count') + 1
                    attraction_popularity.save()
                    # 重新查询以获取最新的 view_count 值
                    attraction_popularity.refresh_from_db()

                results.append({
                    "id": attraction.id,
                    "name": attraction.name,
                    "rating": attraction.rating,
                    "popularity": attraction_popularity.view_count,
                    "description": attraction.description,
                    "location": attraction.province_city_district,
                })

                # 记录搜索历史
                UserSearchHistory.objects.create(user=request.user, attraction=attraction)

        # 根据 category 参数进行排序
        if category == 'rating':
            results = sorted(results, key=lambda x: x['rating'], reverse=True)
        elif category == 'popularity':
            results = sorted(results, key=lambda x: x['popularity'], reverse=True)

        # 返回前10个结果
        sorted_results = results[:10]

        if not sorted_results:
            return Response({"error": "No attractions found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"attractions": sorted_results}, status=status.HTTP_200_OK)

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


import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FacilitySearch(APIView):
    def get(self, request, *args, **kwargs):
        # 读取 node_names.json 文件中的数据
        with open('node_names.json', 'r') as file:
            node_names = json.load(file)
        
        # 获取查询参数
        name = request.GET.get('name')
        facility_type = request.GET.get('type')
        
        # 过滤结果
        filtered_names = []
        for node in node_names:
            if name and name.lower() not in node.lower():
                continue
            if facility_type and not node.startswith(facility_type):
                continue
            filtered_names.append(node)
        
        return Response(filtered_names, status=status.HTTP_200_OK)
    



import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import networkx as nx
from backend.tourist_routes.graph import load_graph_from_json,dijkstra
class NearbyFacilitySearch(APIView):
    def get(self, request, *args, **kwargs):
        # 读取 node_names.json 文件中的数据
        with open(settings.BASE_DIR / 'node_names.json', 'r') as file:
            node_names = json.load(file)

        # 读取图数据
        graph = load_graph_from_json(settings.BASE_DIR / 'graph.json')

        # 获取查询参数
        facility_type = request.GET.get('type')
        location = request.GET.get('location')
        radius = request.GET.get('radius', None)

        # 验证facility_type
        if facility_type not in ['supermarket', 'wc', 'restaurant', 'node', 'others']:
            return Response({"error": "Invalid facility type."}, status=status.HTTP_400_BAD_REQUEST)

        # 过滤设施类型
        facilities = [name for name in node_names if name.startswith(facility_type)]

        if location:
            if location not in graph.nodes:
                return Response({"error": "Invalid location."}, status=status.HTTP_400_BAD_REQUEST)
            # 计算从起点到每个设施的最短路径距离
            facilities_with_distance = []
            for facility in facilities:
                path, distance, _ = dijkstra(graph, location, facility)
                if radius is None or distance <= int(radius):
                    facilities_with_distance.append({"name": facility, "distance": distance})
            facilities = sorted(facilities_with_distance, key=lambda x: x['distance'])
        else:
            facilities = [{"name": facility, "distance": None} for facility in facilities]

        return Response({"facilities": facilities}, status=status.HTTP_200_OK)
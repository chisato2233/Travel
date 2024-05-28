import networkx as nx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings  # 使用Django的设置模块来管理图文件路径

# 假设这些函数在 graph_utils.py 中定义
from .graph import load_graph_from_json, dijkstra,multi_point_dijkstra



class OptimalRouteView(APIView):
    # 加载图数据一次，并存储在类变量中以供所有请求使用
    graph = load_graph_from_json("backend/tourist_routes/data/graph.json")
    def post(self, request, *args, **kwargs):
        start_location = request.data.get("startLocation")
        end_location = request.data.get("endLocation")
        strategy = request.data.get("strategy")

        # 检查节点是否存在于图中
        if not self.graph.has_node(start_location) or not self.graph.has_node(end_location):
            return Response({"error": "Start or end location does not exist in the graph."}, status=status.HTTP_400_BAD_REQUEST)

        if not start_location or not end_location or strategy not in ["shortest", "fastest"]:
            return Response({"error": "Invalid location or strategy."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if strategy == "shortest":
                path, total_distance, total_time = dijkstra(self.graph, start_location, end_location, weight='distance')
            else:
                path, total_distance, total_time = dijkstra(self.graph, start_location, end_location, weight='time')

            return Response({
                "route": path,
                "distance": total_distance,
                "time": total_time
            }, status=status.HTTP_200_OK)
        except nx.NetworkXNoPath:
            return Response({"error": "No path between start and end locations."}, status=status.HTTP_400_BAD_REQUEST)
        

class MultiDestinationRouteView(APIView):
    # 加载图数据一次，并存储在类变量中以供所有请求使用
    graph = load_graph_from_json("backend/tourist_routes/data/graph.json")
    def post(self, request, *args, **kwargs):
        start_location = request.data.get("startLocation")
        end_location = request.data.get("endLocation")
        via_points = request.data.get("viaPoints", [])
        strategy = request.data.get("strategy")

        # 检查节点是否存在于图中
        for location in [start_location, end_location] + via_points:
            if not self.graph.has_node(location):
                return Response({"error": f"Location {location} does not exist in the graph."}, status=status.HTTP_400_BAD_REQUEST)

        if not start_location or not end_location or strategy not in ["shortest", "fastest"]:
            return Response({"error": "Invalid location or strategy."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            points = [start_location] + via_points + [end_location]
            if strategy == "shortest":
                path, total_distance, total_time = multi_point_dijkstra(self.graph, points, weight='distance')
            else:
                path, total_distance, total_time = multi_point_dijkstra(self.graph, points, weight='time')

            return Response({
                "route": path,
                "distance": total_distance,
                "time": total_time
            }, status=status.HTTP_200_OK)
        except nx.NetworkXNoPath:
            return Response({"error": "No path between specified locations."}, status=status.HTTP_400_BAD_REQUEST)
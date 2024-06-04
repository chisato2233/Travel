import networkx as nx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings  # 使用Django的设置模块来管理图文件路径

# 假设这些函数在 graph_utils.py 中定义
from .graph import load_graph_from_json, dijkstra,multi_point_dijkstra

import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from PIL import Image, ImageDraw
import os


class OptimalRouteView(APIView):
    graph = load_graph_from_json("backend/tourist_routes/data/graph.json")

    def post(self, request, *args, **kwargs):
        start_location = request.data.get("startLocation")
        end_location = request.data.get("endLocation")
        strategy = request.data.get("strategy")

        if not self.graph.has_node(start_location) or not self.graph.has_node(end_location):
            return Response({"error": "Start or end location does not exist in the graph."}, status=status.HTTP_400_BAD_REQUEST)

        if not start_location or not end_location or strategy not in ["shortest", "fastest"]:
            return Response({"error": "Invalid location or strategy."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if strategy == "shortest":
                path, total_distance, total_time = dijkstra(self.graph, start_location, end_location, weight='distance')
            else:
                path, total_distance, total_time = dijkstra(self.graph, start_location, end_location, weight='time')

            steps = [
                {"from": path[i], "to": path[i + 1], "time": self.graph[path[i]][path[i + 1]]['time'], "distance": self.graph[path[i]][path[i + 1]]['distance']}
                for i in range(len(path) - 1)
            ]

            return Response({
                "route": path,
                "distance": total_distance,
                "time": total_time,
                "steps": steps
            }, status=status.HTTP_200_OK)
        except nx.NetworkXNoPath:
            return Response({"error": "No path between start and end locations."}, status=status.HTTP_400_BAD_REQUEST)

class MultiDestinationRouteView(APIView):
    graph = load_graph_from_json("backend/tourist_routes/data/graph.json")

    def post(self, request, *args, **kwargs):
        start_location = request.data.get("startLocation")
        end_location = request.data.get("endLocation")
        via_points = request.data.get("viaPoints", [])
        strategy = request.data.get("strategy")

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

            steps = [
                {"from": path[i], "to": path[i + 1], "time": self.graph[path[i]][path[i + 1]]['time'], "distance": self.graph[path[i]][path[i + 1]]['distance']}
                for i in range(len(path) - 1)
            ]

            return Response({
                "route": path,
                "distance": total_distance,
                "time": total_time,
                "steps": steps
            }, status=status.HTTP_200_OK)
        except nx.NetworkXNoPath:
            return Response({"error": "No path between specified locations."}, status=status.HTTP_400_BAD_REQUEST)
# views.py

from django.http import JsonResponse
from django.conf import settings

def get_global_map(request):
    image_url = f"{settings.MEDIA_URL}tourist_routes/graph_visualization.png"
    return JsonResponse({"image_url": request.build_absolute_uri(image_url)})





def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = json_graph.node_link_graph(data)
    return G

def draw_graph(G, file_path):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20), dpi=300)
    
    # Save the positions for later use
    nx.set_node_attributes(G, pos, 'pos')
    
    # 绘制原图
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color='blue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='black')
    
    plt.title('Graph Visualization')
    plt.savefig(file_path, format="PNG")
    plt.close()

class RoutesImageView(View):
    graph = load_graph_from_json("backend/tourist_routes/data/graph.json")
    original_image_output_path = os.path.join(settings.MEDIA_ROOT, "tourist_routes", "graph_visualization.png")
    route_image_output_path = os.path.join(settings.MEDIA_ROOT, "tourist_routes", "route_image.png")
    
    # 生成并保存整体图像
    draw_graph(graph, original_image_output_path)

    @staticmethod
    def draw_route_on_blank_graph(G, route, file_path):
        pos = nx.get_node_attributes(G, 'pos')
        if not pos:
            raise ValueError("Graph does not have node positions")

        plt.figure(figsize=(20, 20), dpi=300)

        # Ensure all route nodes have positions
        for node in route:
            if node not in pos:
                raise ValueError(f"Node '{node}' has no position.")

        # 仅绘制路径和所用节点
        route_nodes = set(route)
        path_edges = list(zip(route, route[1:]))
        
        # 绘制路径上的节点
        nx.draw_networkx_nodes(G, pos, nodelist=route_nodes, node_size=10, node_color='red')
        
        # 绘制路径
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        
        # 绘制路径上的节点标签
        nx.draw_networkx_labels(G, pos, labels={node: node for node in route_nodes}, font_size=5, font_color='black')
        
        plt.title('Route Visualization')
        plt.savefig(file_path, format="PNG")
        plt.close()

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            data = json.loads(request.body)
            route = data.get("route", [])

            if not route:
                return JsonResponse({"error": "No route provided."}, status=400)

            # 生成并保存包含路径的图像
            self.draw_route_on_blank_graph(self.graph, route, self.route_image_output_path)
            image_path = os.path.join(settings.MEDIA_URL, 'tourist_routes/route_image.png')
            image_url = request.build_absolute_uri(image_path)
            return JsonResponse({"image_url": image_url}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
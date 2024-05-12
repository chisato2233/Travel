# import networkx as nx
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings  # 使用Django的设置模块来管理图文件路径

# # 假设这些函数在 graph_utils.py 中定义
# from .graph import load_graph_from_json, dijkstra

# class OptimalRouteView(APIView):
#     # 加载图数据一次，并存储在类变量中以供所有请求使用
#     graph = load_graph_from_json("./data/graph.json")

#     def post(self, request, *args, **kwargs):
#         start_location = request.data.get("startLocation")
#         end_location = request.data.get("endLocation")
#         strategy = request.data.get("strategy")

#         # 检查节点是否存在于图中
#         if not self.graph.has_node(start_location) or not self.graph.has_node(end_location):
#             return Response({"error": "Start or end location does not exist in the graph."}, status=status.HTTP_400_BAD_REQUEST)

#         if not start_location or not end_location or strategy not in ["shortest", "fastest"]:
#             return Response({"error": "Invalid location or strategy."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             if strategy == "shortest":
#                 path, length = dijkstra(self.graph, start_location, end_location)
#             else:
#                 # 这里可以添加对“fastest”策略的具体实现
#                 path = nx.shortest_path(self.graph, source=start_location, target=end_location, weight='weight')
#                 length = sum(self.graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))

#             # 假设平均速度为50km/h，计算时间
#             average_speed = 50
#             time_hours = length / average_speed

#             return Response({
#                 "route": path,
#                 "distance": length,
#                 "time": "{} hours".format(time_hours)
#             }, status=status.HTTP_200_OK)
#         except nx.NetworkXNoPath:
#             return Response({"error": "No path between start and end locations."}, status=status.HTTP_400_BAD_REQUEST)

# # 在 settings.py 中添加 GRAPH_JSON_PATH
# # GRAPH_JSON_PATH = 'path_to_your_graph_data.json'

import json
import networkx as nx
from networkx.readwrite import json_graph

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = json_graph.node_link_graph(data)
    return G


import heapq


def dijkstra(G, start, end, weight='distance'):
    # 初始化距离字典，所有节点距离无穷大，除了起点为0
    distances = {vertex: float('infinity') for vertex in G.nodes}
    distances[start] = 0
    
    # 初始化前驱节点字典，用于记录最短路径
    predecessors = {vertex: None for vertex in G.nodes}
    
    # 优先队列，用于选取当前距离最小的节点，初始包含起点
    priority_queue = [(0, start)]
    
    while priority_queue:
        # 弹出当前距离最小的节点
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # 如果当前节点就是终点，则停止算法
        if current_vertex == end:
            break

        # 遍历当前节点的邻居
        for neighbor in G.neighbors(current_vertex):
            weight_value = G.edges[current_vertex, neighbor].get(weight, 1)
            distance = current_distance + weight_value
            
            # 如果找到更短的路径，则更新距离和前驱节点，然后将邻居节点加入队列
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # 回溯前驱节点字典构造最短路径
    path = []
    total_distance = 0
    total_time = 0
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        if predecessors[current_vertex] is not None:
            edge_data = G.edges[predecessors[current_vertex], current_vertex]
            total_distance += edge_data.get('distance', 0)
            total_time += edge_data.get('time', 0)
        current_vertex = predecessors[current_vertex]
    path.reverse()

    return path, total_distance, total_time



def multi_point_dijkstra(G, points, weight='distance'):
    if not points:
        return [], 0, 0

    total_path = []
    total_distance = 0
    total_time = 0

    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        path, distance, time = dijkstra(G, start, end, weight)
        if not total_path:
            total_path.extend(path)
        else:
            total_path.extend(path[1:])
        total_distance += distance
        total_time += time

    return total_path, total_distance, total_time
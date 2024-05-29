import json
import random

def generate_graph(num_nodes):
    graph = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": [],
        "links": []
    }

    # 生成节点
    for i in range(num_nodes):
        node_id = chr(ord('A') + i) if i < 26 else 'Node' + str(i)
        graph["nodes"].append({"id": node_id})

    # 创建一个连通的骨架图，确保没有孤岛
    nodes = [node["id"] for node in graph["nodes"]]
    random.shuffle(nodes)
    
    for i in range(len(nodes) - 1):
        distance = random.randint(1, 100)  # 以公里为单位
        speed = random.uniform(50, 100)  # 速度范围在50到100公里/小时之间
        time = round(distance / speed * 60)  # 以分钟为单位
        graph["links"].append({
            "source": nodes[i],
            "target": nodes[i + 1],
            "distance": distance,
            "time": time
        })

    # 添加更多的随机边
    extra_edges = num_nodes * 2  # 增加一些额外的边
    while len(graph["links"]) < extra_edges:
        source = random.choice(nodes)
        target = random.choice(nodes)
        if source != target and not any(link for link in graph["links"] if (link["source"] == source and link["target"] == target) or (link["source"] == target and link["target"] == source)):
            distance = random.randint(1, 100)
            speed = random.uniform(50, 100)
            time = round(distance / speed * 60)
            graph["links"].append({
                "source": source,
                "target": target,
                "distance": distance,
                "time": time
            })

    return graph

def save_graph_to_json(graph, file_path):
    with open(file_path, 'w') as f:
        json.dump(graph, f, indent=2)

if __name__ == "__main__":
    num_nodes = 200  # 节点数量

    graph = generate_graph(num_nodes)
    save_graph_to_json(graph, "graph.json")
    print("Graph with 200 nodes has been generated and saved to graph.json")

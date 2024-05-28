import json
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = json_graph.node_link_graph(data)
    return G

def draw_graph(G, file_path):
    pos = nx.spring_layout(G)  # 使用spring布局
    plt.figure(figsize=(20, 20), dpi=300)  # 调整图像大小和分辨率
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color='blue')
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='black')
    
    plt.title('Graph Visualization')
    plt.savefig(file_path, format="PNG")
    plt.show()

if __name__ == "__main__":
    graph_json_path = "graph.json"  # 替换为你的JSON文件路径
    image_output_path = "graph_visualization.png"
    
    G = load_graph_from_json(graph_json_path)
    draw_graph(G, image_output_path)
    print(f"Graph visualization has been saved to {image_output_path}")

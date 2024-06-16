import pydotplus
from collections import namedtuple

# 定义模型类
Class = namedtuple('Class', ['name', 'fields', 'methods'])

# 定义类及其属性和方法
user = Class(
    name='User',
    fields=['id: Integer', 'username: String', 'is_authenticated: Boolean'],
    methods=[]
)

user_search_history = Class(
    name='UserSearchHistory',
    fields=['id: Integer', 'user: ForeignKey(User)', 'attraction: ForeignKey(Attraction)', 'search_time: DateTime'],
    methods=[]
)

attraction = Class(
    name='Attraction',
    fields=['id: Integer', 'name: String', 'description: Text', 'rating: Float', 'popularity: Integer (Optional)'],
    methods=[]
)

diary_entry = Class(
    name='DiaryEntry',
    fields=['id: Integer', 'title: String', 'content: Text', 'date: Date', 'location: String', 'user: ForeignKey(User)', 'rating: Float (Optional)'],
    methods=[]
)

diary_rating = Class(
    name='DiaryRating',
    fields=['id: Integer', 'user: ForeignKey(User)', 'diary_entry: ForeignKey(DiaryEntry)', 'rating: Float'],
    methods=[]
)

classes = [user, user_search_history, attraction, diary_entry, diary_rating]

# 创建UML图
graph = pydotplus.Dot(graph_type='digraph', rankdir='LR')

# 添加类节点
for cls in classes:
    label = f"{cls.name}|{'|'.join(cls.fields)}"
    node = pydotplus.Node(cls.name, shape='record', label='{'+label+'}')
    graph.add_node(node)

# 添加关系
relations = [
    ('UserSearchHistory', 'User'),
    ('UserSearchHistory', 'Attraction'),
    ('DiaryEntry', 'User'),
    ('DiaryRating', 'User'),
    ('DiaryRating', 'DiaryEntry')
]

for rel in relations:
    edge = pydotplus.Edge(rel[0], rel[1])
    graph.add_edge(edge)

# 保存为PDF文件
graph.write_pdf('uml_diagram.pdf')

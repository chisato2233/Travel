# 游学系统






文件结构：

```
Travel/
│
├── backend/
│   ├── authentication/       # 处理用户认证相关的逻辑
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── recommendations/      # 处理游学推荐相关的逻辑
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── routes/               # 处理游学路线规划相关的逻辑
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── search/               # 处理各类查询相关的逻辑
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── diaries/              # 处理游学日记管理相关的逻辑
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── travel/    # Django项目的主要配置目录
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
|
|
......

```

# 数据库信息（可以直接和ai说）
```
我的景点数据库在数据库中已经存放，表名sheet，表项有：
id int
城市 text
名称 text
星级 text
评分 double
价格 double
销量 int
省/市/区 text
坐标 text
简介 text
是否免费 text
具体地址 text
```
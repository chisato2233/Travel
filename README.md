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

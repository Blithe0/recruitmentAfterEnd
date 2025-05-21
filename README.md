recruitment_system/
├── app/
│   ├── models/              # SQLAlchemy 模型
│   │   ├── user.py
│   │   ├── demand.py
│   │   └── ...
│   ├── routes/              # 路由（API）
│   │   ├── user.py
│   │   ├── demand.py
│   │   ├── auth.py
│   │   └── ...
│   ├── services/            # 业务逻辑
│   ├── schemas/             # 请求/响应数据结构 (pydantic-like)
│   ├── __init__.py
│   └── extensions.py        # 数据库、CORS、JWT等插件初始化
├── config.py
├── run.py
├── README.md
└── requirements.txt

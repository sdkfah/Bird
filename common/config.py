import os
from dotenv import load_dotenv

# 加载 .env 文件中的变量
load_dotenv()

class Config:
    # 数据库配置
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASS", ""),
        "database": os.getenv("DB_NAME", "tickets"),
        "charset": os.getenv("DB_CHARSET", "utf8mb4")
    }

    # 其他配置
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 10))

# 创建一个全局配置实例
config = Config()
import os
import yaml
import pymysql
from jinja2 import Environment, BaseLoader
from dbutils.pooled_db import PooledDB
from loguru import logger
from common.config import config


class BaseRepository:
    def __init__(self, mapper_dir):
        """
        新版初始化：使用原生 Jinja2 替代 jinjasql
        """
        # 1. 初始化 Jinja2 环境 (用于渲染动态 SQL 逻辑)
        self.jinja_env = Environment(loader=BaseLoader())
        self.mappers = {}

        # 2. 初始化数据库连接池
        db_params = config.DB_CONFIG
        try:
            self.pool = PooledDB(
                creator=pymysql,
                mincached=5,
                maxcached=20,
                maxconnections=100,
                blocking=True,
                setsession=['SET AUTOCOMMIT = 1'],
                host=db_params["host"],
                port=db_params["port"],
                user=db_params["user"],
                password=db_params["password"],
                database=db_params["database"],
                charset=db_params["charset"],
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("✅ 数据库连接池初始化成功 (原生 Jinja2 模式)")
        except Exception as e:
            logger.error(f"❌ 数据库池初始化失败: {e}")
            raise

        # 3. 使用 PyYAML 加载 Mapper 文件
        self._load_mappers(mapper_dir)

    def _load_mappers(self, mapper_dir):
        """利用 PyYAML 扫描并解析所有 SQL 模板 """
        if not os.path.exists(mapper_dir):
            return

        for filename in os.listdir(mapper_dir):
            if filename.endswith(('.yaml', '.yml')):
                file_path = os.path.join(mapper_dir, filename)
                namespace = os.path.splitext(filename)[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # PyYAML 将文件内容解析为字典
                        content = yaml.safe_load(f)
                        if content:
                            self.mappers[namespace] = content
                    logger.info(f"📑 已加载 Mapper: {namespace}")
                except Exception as e:
                    logger.error(f"❌ 加载 Mapper {filename} 失败: {e}")

    def execute(self, namespace, sql_id, params=None):
        """
        执行 SQL：先用 Jinja2 渲染，再由 PyMySQL 执行
        """
        params = params or {}

        # 1. 获取 SQL 模板
        mapper = self.mappers.get(namespace)
        if not mapper: raise ValueError(f"Namespace {namespace} missing")
        template_str = mapper.get(sql_id)
        if not template_str: raise ValueError(f"SQL ID {sql_id} missing")

        # 2. 使用 Jinja2 渲染动态 SQL (处理 if/for 等逻辑)
        # 注意：为了安全，复杂场景建议改用参数化构建，这里演示核心逻辑
        template = self.jinja_env.from_string(template_str)
        query = template.render(**params)

        # 3. 从连接池获取连接并执行
        conn = self.pool.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)  # 直接执行渲染后的 SQL
                conn.commit()

                # 自动处理返回类型
                q_upper = query.strip().upper()
                if q_upper.startswith(("SELECT", "SHOW", "DESC")):
                    return cursor.fetchall()
                return {"affected": cursor.rowcount, "last_id": cursor.lastrowid}
        finally:
            conn.close()
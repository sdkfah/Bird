import os
import yaml
import pymysql
from jinja2 import Environment, BaseLoader
from dbutils.pooled_db import PooledDB
from loguru import logger
from common.config import config

class BaseRepository:
    # --- 类变量：所有子类共享的单例资源 ---
    _pool = None
    _mappers = {}      # 缓存 SQL 模板，避免重复磁盘 IO
    _jinja_env = None  # 共享渲染引擎

    def __init__(self, mapper_dir):
        # 1. 确保连接池全局唯一
        if BaseRepository._pool is None:
            self._init_pool()
        self.pool = BaseRepository._pool

        # 2. 确保 Jinja2 环境全局唯一
        if BaseRepository._jinja_env is None:
            BaseRepository._jinja_env = Environment(loader=BaseLoader())
        self.jinja_env = BaseRepository._jinja_env

        # 3. 确保 Mapper 全局只加载一次
        if not BaseRepository._mappers:
            self._load_all_mappers(mapper_dir)
        self.mappers = BaseRepository._mappers

    def _init_pool(self):
        """初始化数据库连接池"""
        db_params = config.DB_CONFIG
        try:
            BaseRepository._pool = PooledDB(
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
            logger.info("✅ 全局数据库连接池初始化成功")
        except Exception as e:
            logger.error(f"❌ 数据库池初始化失败: {e}")
            raise

    def _load_all_mappers(self, mapper_dir):
        """扫描并解析所有 YAML 逻辑到类变量"""
        if not os.path.exists(mapper_dir):
            return

        for filename in os.listdir(mapper_dir):
            if filename.endswith(('.yaml', '.yml')):
                file_path = os.path.join(mapper_dir, filename)
                namespace = os.path.splitext(filename)[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f)
                        if content:
                            BaseRepository._mappers[namespace] = content # 存入类变量
                    logger.info(f"📑 成功加载 Mapper: {namespace}")
                except Exception as e:
                    logger.error(f"❌ 加载 Mapper {filename} 失败: {e}")

    def execute(self, namespace, sql_id, params=None):
        """执行 SQL：先由 Jinja2 处理逻辑，再由 PyMySQL 参数化执行"""
        params = params or {}
        mapper = self.mappers.get(namespace)
        if not mapper: raise ValueError(f"Namespace {namespace} missing")

        template_str = mapper.get(sql_id)
        if not template_str: raise ValueError(f"SQL ID {sql_id} missing")

        # --- 修复逻辑开始 ---
        # 1. 第一步：Jinja2 渲染（处理 if/for 等逻辑，但不替换 %(key)s）
        # 注意：此时 template_str 里的 %(name)s 会被保留
        query = self.jinja_env.from_string(template_str).render(**params)

        conn = self.pool.connection()
        try:
            with conn.cursor() as cursor:
                # 2. 第二步：将渲染后的 SQL 和原始 params 一起传给 execute
                # PyMySQL 会自动匹配 SQL 里的 %(key)s 并安全地替换 params 里的值
                cursor.execute(query, params)
                # --- 修复逻辑结束 ---

                conn.commit()
                q_upper = query.strip().upper()
                if q_upper.startswith(("SELECT", "SHOW", "DESC")):
                    return cursor.fetchall()
                return {"affected": cursor.rowcount, "last_id": cursor.lastrowid}
        finally:
            conn.close()
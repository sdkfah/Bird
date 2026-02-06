import os
import yaml
import pymysql
from dbutils.pooled_db import PooledDB
from jinjasql import JinjaSql
from loguru import logger
from common.config import config

class BaseRepository:
    def __init__(self, mapper_dir):
        """
        初始化数据库连接池并加载所有 SQL 映射文件
        :param mapper_dir: mappers 目录的绝对路径
        """
        self.j = JinjaSql(param_style='pyformat')
        self.mappers = {}

        # 1. 初始化数据库连接池 (适应高并发)
        db_params = config.DB_CONFIG
        try:
            self.pool = PooledDB(
                creator=pymysql,
                mincached=5,  # 启动时最少空闲连接数
                maxcached=20,  # 最大空闲连接数
                maxconnections=100,  # 最大允许连接数
                blocking=True,  # 连接池满时是否阻塞等待
                host=db_params["host"],
                port=db_params["port"],
                user=db_params["user"],
                password=db_params["password"],
                database=db_params["database"],
                charset=db_params["charset"],
                cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的结果
            )
            logger.info("✅ 数据库连接池初始化成功")
        except Exception as e:
            logger.error(f"❌ 数据库连接池初始化失败: {e}")
            raise

        # 2. 加载 Mapper 文件
        self._load_mappers(mapper_dir)

    def _load_mappers(self, mapper_dir):
        """扫描并解析 mappers 文件夹下的所有 yaml 文件"""
        if not os.path.exists(mapper_dir):
            logger.warning(f"⚠️ Mapper 目录不存在: {mapper_dir}")
            return

        for filename in os.listdir(mapper_dir):
            if filename.endswith(('.yaml', '.yml')):
                file_path = os.path.join(mapper_dir, filename)
                namespace = os.path.splitext(filename)[0]
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f)
                        if content:
                            self.mappers[namespace] = content
                    logger.info(f"📑 已加载 Mapper: {namespace}")
                except Exception as e:
                    logger.error(f"❌ 加载 Mapper {filename} 失败: {e}")

    def execute(self, namespace, sql_id, params=None):
        """
        执行 SQL (自动渲染动态 SQL)
        :param namespace: yaml 文件名 (不带后缀)
        :param sql_id: yaml 里的 key
        :param params: 字典格式的参数
        """
        if params is None:
            params = {}

        # 1. 获取 SQL 模板
        mapper = self.mappers.get(namespace)
        if not mapper:
            raise ValueError(f"Namespace '{namespace}' 不存在")

        template = mapper.get(sql_id)
        if not template:
            raise ValueError(f"SQL ID '{sql_id}' 在 {namespace} 中未找到")

        # 2. 使用 JinjaSql 渲染动态 SQL (防止 SQL 注入)
        query, bind_params = self.j.prepare_query(template, params)

        # 3. 从连接池获取连接并执行
        conn = self.pool.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, bind_params)
                conn.commit()
                return cursor.fetchall()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ SQL 执行异常 [{namespace}.{sql_id}]: {e}")
            raise
        finally:
            conn.close()  # 归还连接到连接池
# data/db_handler.py
import os

import pymysql
import inspect  # 用于清理 SQL 缩进
from config import DB_CONFIG
from datetime import datetime

class DBHandler:
    def __init__(self):
        self.config = DB_CONFIG
        # 获取 sql 文件夹的绝对路径
        self.sql_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sqls"
        )

    def _get_conn(self):
        return pymysql.connect(**self.config)

    def _load_sql(self, filename):
        """读取 SQL 文件内容"""
        file_path = os.path.join(self.sql_base_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def init_tables(self):
        """从文件加载并执行建表语句"""
        # 如果一个文件里有多个 SQL 语句，需要 split(';') 执行
        full_sql = self._load_sql("init_tables.sql")
        sqls = [s.strip() for s in full_sql.split(';') if s.strip()]

        conn = self._get_conn()
        try:
            with conn.cursor() as cursor:
                for sql in sqls:
                    cursor.execute(sql)
            conn.commit()
            print("[*] 数据库表初始化成功（从文件加载）。")
        finally:
            conn.close()

    def upsert_ticket_items(self, rows_dicts):
        """
        rows_dicts: 列表包含字典，键名需与 SQL 里的 %(key)s 一致
        """
        sql = self._load_sql("upsert_ticket_items")
        conn = self._get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, rows_dicts)
            conn.commit()
        finally:
            conn.close()

    def find_matching_orders(self, project_title, price_name):
        sql = self._load_sql("find_matching_orders")
        conn = self._get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 使用字典传参
                cursor.execute(sql, {"project_title": project_title, "price_name": price_name})
                return cursor.fetchall()
        finally:
            conn.close()

    def insert_parsed_tasks(self, task_list):
        sql = self._load_sql("insert_parsed_tasks")
        beijing_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 为每条数据添加创建时间
        for t in task_list:
            t['created_at'] = beijing_now

        conn = self._get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, task_list)
            conn.commit()
        finally:
            conn.close()

    def get_matched_tasks_report(self, artist_name=None):
        sql = self._load_sql("get_matched_tasks_report")

        if artist_name:
            sql += " AND t.artist = %(artist_name)s"

        sql += " ORDER BY t.bounty DESC, t.created_at ASC"

        conn = self._get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, {"artist_name": artist_name})
                return cursor.fetchall()
        finally:
            conn.close()
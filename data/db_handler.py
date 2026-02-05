# data/db_handler.py
import pymysql
import inspect  # 用于清理 SQL 缩进
from config import DB_CONFIG
from datetime import datetime

class DBHandler:
    def __init__(self):
        self.config = DB_CONFIG

    def _get_conn(self):
        return pymysql.connect(**self.config)

    def init_tables(self):
        # 使用 cleandoc 清理多行字符串的缩进
        order_tasks_sql = inspect.cleandoc("""
            CREATE TABLE IF NOT EXISTS `order_tasks` (
              `id` int NOT NULL AUTO_INCREMENT,
              `project_keyword` varchar(128) NOT NULL COMMENT '项目关键词',
              `target_date` varchar(64) DEFAULT NULL COMMENT '目标日期',
              `target_price` varchar(128) DEFAULT NULL COMMENT '目标票价',
              `customer_info` varchar(500) DEFAULT NULL COMMENT '实名人信息(姓名+身份证)',
              `priority_order` varchar(255) DEFAULT NULL COMMENT '优先顺序',
              `bounty` decimal(10,2) DEFAULT NULL COMMENT '红包金额',
              `contact_phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
              `status` tinyint DEFAULT '0' COMMENT '状态: 0待处理, 1已抢到, 2已撤单',
              `created_at` datetime DEFAULT NULL COMMENT '创建时间',
              PRIMARY KEY (`id`),
              UNIQUE KEY `uk_project_customer` (`project_keyword`,`customer_info`),
              KEY `idx_project_status` (`project_keyword`,`status`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        ticket_items_sql = inspect.cleandoc("""
            CREATE TABLE IF NOT EXISTS `ticket_items` (
              `id` bigint NOT NULL AUTO_INCREMENT,
              `item_id` varchar(32) NOT NULL COMMENT '项目ID',
              `project_title` varchar(255) DEFAULT NULL COMMENT '演出名称',
              `venue_name` varchar(128) DEFAULT NULL COMMENT '场馆',
              `perform_id` varchar(32) NOT NULL COMMENT '场次ID',
              `perform_time` datetime DEFAULT NULL COMMENT '演出时间',
              `sku_id` varchar(32) NOT NULL COMMENT '票档SKU ID',
              `price_name` varchar(64) DEFAULT NULL COMMENT '票档描述',
              `price` decimal(10,2) DEFAULT NULL COMMENT '价格',
              `stock_status` tinyint(1) DEFAULT '1' COMMENT '是否有票: 1有, 0无',
              `limit_quantity` int DEFAULT '4' COMMENT '每单限购额',
              `sale_start_time` datetime DEFAULT NULL COMMENT '开抢时间',
              `updated_at` datetime DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `sku_id` (`sku_id`),
              KEY `idx_perform_sku` (`perform_id`,`sku_id`),
              KEY `idx_sale_time` (`sale_start_time`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        conn = self._get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(order_tasks_sql)
                cursor.execute(ticket_items_sql)
            conn.commit()
            print("[*] 数据库表初始化完成，SQL 格式已自动对齐。")
        finally:
            conn.close()

    def upsert_ticket_items(self, rows):
        sql = """
        INSERT INTO `ticket_items` (
            item_id, project_title, venue_name, perform_id, perform_time,
            sku_id, price_name, price, stock_status, limit_quantity, 
            sale_start_time, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE
            stock_status = VALUES(stock_status),
            price        = VALUES(price),
            updated_at   = VALUES(updated_at);
        """
        conn = self._get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, rows)
            conn.commit()
        finally:
            conn.close()

    def find_matching_orders(self, project_title, price_name):
        """狙击匹配：寻找红包最高且符合项目和票价的任务"""
        sql = """
        SELECT customer_info, bounty, contact_phone
        FROM order_tasks
        WHERE %s LIKE CONCAT('%%', project_keyword, '%%')
          AND %s LIKE CONCAT('%%', target_price, '%%')
          AND status = 0
        ORDER BY bounty DESC 
        """
        conn = self._get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, (project_title, price_name))
                return cursor.fetchall()
        finally:
            conn.close()

    def insert_parsed_tasks(self, task_list):
        """批量录入 Parser 转换后的报单数据"""
        sql = """
            INSERT INTO `order_tasks` (
            project_keyword, target_date, target_price, customer_info, 
            priority_order, bounty, contact_phone, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            bounty = VALUES(bounty), 
            contact_phone = VALUES(contact_phone),
            target_price = VALUES(target_price)
              """
        conn = self._get_conn()
        beijing_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with conn.cursor() as cursor:
                data = [
                    (t['keyword'], t['date'], t['price'], t['info'],
                     t['priority'], t['bounty'], t['phone'], beijing_now)
                    for t in task_list
                ]
                cursor.executemany(sql, data)
            conn.commit()
        finally:
            conn.close()
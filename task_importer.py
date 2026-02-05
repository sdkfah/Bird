# task_importer.py
import sys
import os

# 确保程序能找到 core 和 data 包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.db_handler import DBHandler
import pprint


def import_tasks():
    tasks = []

    if not tasks:
        print("[-] 未识别到有效订单，请检查格式。")
        return

    pprint.pprint(tasks)

    # 3. 调用数据包的处理器存入 MySQL
    db = DBHandler()
    db.insert_parsed_tasks(tasks)


if __name__ == "__main__":
    import_tasks()

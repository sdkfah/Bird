from .base_repo import BaseRepository
from loguru import logger

class DeviceRepository(BaseRepository):
    def __init__(self, mapper_dir):
        super().__init__(mapper_dir)

    # --- 设备基础操作 ---

    def register_device(self, device_data: dict):
        """
        注册或更新设备状态 (upsert 逻辑)
        device_data 包含: sn, brand, model, ip_address, status
        """
        try:
            return self.execute("device_mapper", "upsert_device", device_data)
        except Exception as e:
            logger.error(f"设备注册失败: {e}")
            raise

    def get_device_config(self, sn: str):
        """
        获取设备详情及其所属分组的 JSON 配置
        """
        result = self.execute("device_mapper", "get_device_with_config", {"sn": sn})
        return result[0] if result else None

    def update_heartbeat(self, sn: str):
        """
        更新设备心跳，防止被识别为离线
        """
        return self.execute("device_mapper", "heartbeat", {"sn": sn})

    # --- 分组 CRUD ---

    def create_group(self, name: str, config: dict, desc: str = ""):
        """创建新设备组"""
        import json
        params = {
            "name": name,
            "config_json": json.dumps(config),
            "description": desc
        }
        return self.execute("device_mapper", "insert_group", params)

    def get_all_groups(self):
        """获取所有分组列表"""
        return self.execute("device_mapper", "get_all_groups")

    def delete_group(self, group_id: int):
        """删除分组"""
        # 建议先在业务层判断该组下是否有设备，或在 SQL 中处理级联
        return self.execute("device_mapper", "delete_group", {"id": group_id})

    # --- 核心业务：一键迁移与批量关联 ---

    def migrate_devices_to_group(self, sn_list: list, target_group_id: int):
        """
        批量迁移设备到新分组（逻辑事务处理）
        """
        success_count = 0
        for sn in sn_list:
            try:
                # 1. 清除当前所有关联
                self.execute("device_mapper", "clear_device_links", {"sn": sn})
                # 2. 绑定至新分组
                self.execute("device_mapper", "batch_link_to_group", {
                    "sn": sn,
                    "group_id": target_group_id
                })
                success_count += 1
            except Exception as e:
                logger.error(f"设备 {sn} 迁移失败: {e}")
                # 此处可以调用 db_log.error 记录到 action_logs 表
        return success_count

    def get_group_members(self, group_id: int):
        """查看某个分组下的所有手机"""
        return self.execute("device_mapper", "get_devices_in_group", {"group_id": group_id})

    # --- 集群运维 ---

    def clean_zombie_devices(self, minutes: int = 5):
        """
        清理僵尸设备：将超过指定分钟未心跳的设备置为离线
        """
        return self.execute("device_mapper", "auto_offline_devices", {"minutes": minutes})
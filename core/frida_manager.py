import frida
from loguru import logger


class FridaManager:
    def __init__(self, device_sn):
        self.device_sn = device_sn
        self.session = None

    def run_agent(self, on_message_callback):
        try:
            device = frida.get_device(self.device_sn)
            self.session = device.attach("大麦")

            with open("scripts/agent.js", "r", encoding="utf-8") as f:
                script = self.session.create_script(f.read())

            script.on('message', on_message_callback)
            script.load()
            logger.info(f"[*] 设备 {self.device_sn} 监听已启动")
        except Exception as e:
            logger.error(f"[-] 设备 {self.device_sn} 连接失败: {e}")
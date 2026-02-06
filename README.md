

## 📂 项目目录结构

```text
Bird/
├── common/                 # 全局通用工具
│   ├── logger.py           # 基于 loguru 的日志封装
│   └── config.py           # 读取 .env 或 yaml 配置文件
├── core/                   # 底层驱动层 (Hardware/Driver Layer)
│   ├── adb_client.py       # 封装 ADB 操作 (push, shell, screencap)
│   ├── frida_manager.py    # 封装 frida-inject 指令生成与注入逻辑
│   └── scheduler.py        # 线程池/异步任务调度中心 (ThreadPoolExecutor)
├── mappers/                # SQL 映射层 (MyBatis 风格)
│   ├── device_mapper.yaml  # 设备增删改查 SQL
│   └── group_mapper.yaml   # 分组与配置相关 SQL
├── repository/             # 数据访问层 (Data Access Layer)
│   ├── base_repo.py        # 加载 YAML + JinjaSql 的基类
│   └── device_repo.py      # 调用 SQL 执行结果并返回对象/字典
├── services/               # 业务逻辑层 (Business Layer)
│   ├── deploy_service.py   # 核心：处理“查询分组 -> 准备 JSON -> 批量推送 -> 启动 Frida”
│   └── group_service.py    # 处理分组逻辑
├── web/                    # 界面层 (UI Layer)
│   ├── app.py              # Streamlit 主程序
│   └── components/         # 自定义 UI 组件
├── scripts/                # Frida JS 脚本存放处
│   └── agent.js            # 你的抢票 Hook 脚本
├── .env                    # 数据库密码、IP 等敏感信息
├── requirements.txt        # 项目依赖
└── main.py                 # (可选) 命令行入口
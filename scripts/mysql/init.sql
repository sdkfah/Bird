-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS tickets DEFAULT CHARACTER SET utf8mb4;
USE tickets;

-- ========================================================
-- 1. 业务核心表：库存监控
-- ========================================================
CREATE TABLE IF NOT EXISTS ticket_items (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    item_id         VARCHAR(32)          NOT NULL COMMENT '项目ID',
    project_title   VARCHAR(255)         NULL     COMMENT '演出名称',
    venue_name      VARCHAR(128)         NULL     COMMENT '场馆',
    perform_id      VARCHAR(32)          NOT NULL COMMENT '场次ID',
    perform_time    DATETIME             NULL     COMMENT '演出时间',
    sku_id          VARCHAR(32)          NOT NULL COMMENT '票档SKU ID',
    price_name      VARCHAR(64)          NULL     COMMENT '票档描述',
    price           DECIMAL(10, 2)       NULL     COMMENT '价格',
    stock_status    TINYINT(1) DEFAULT 1 NULL     COMMENT '是否有票: 1有, 0无',
    limit_quantity  INT        DEFAULT 4 NULL     COMMENT '每单限购额',
    sale_start_time DATETIME             NULL     COMMENT '开抢时间',
    updated_at      DATETIME             NULL,
    UNIQUE KEY uk_sku (sku_id),
    INDEX idx_perform_sku (perform_id, sku_id),
    INDEX idx_price_time (price, perform_time),
    INDEX idx_sale_time (sale_start_time)
) ENGINE=InnoDB COMMENT='库存监控表';

-- ========================================================
-- 2. 业务核心表：抢票任务
-- ========================================================
CREATE TABLE IF NOT EXISTS order_tasks (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    city           VARCHAR(64)       NOT NULL COMMENT '城市',
    artist         VARCHAR(128)      NOT NULL COMMENT '艺人/演出名称',
    target_date    DATE              NULL     COMMENT '目标日期',
    target_price   DECIMAL(10, 2)    NULL     COMMENT '目标票价',
    customer_info  VARCHAR(500)      NULL     COMMENT '实名人信息(姓名+身份证)',
    priority_order VARCHAR(255)      NULL     COMMENT '优先顺序',
    bounty         DECIMAL(10, 2)    NULL     COMMENT '红包金额',
    contact_phone  VARCHAR(20)       NULL     COMMENT '联系电话',
    status         TINYINT DEFAULT 0 NULL     COMMENT '状态: 0待处理, 1已抢到, 2已撤单',
    created_at     DATETIME          NULL     COMMENT '创建时间',
    UNIQUE KEY uk_artist_customer (artist, customer_info),
    INDEX idx_status (status)
) ENGINE=InnoDB COMMENT='抢票订单任务表';

-- ========================================================
-- 3. 管理扩展表：设备主表
-- ========================================================
CREATE TABLE IF NOT EXISTS devices (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sn              VARCHAR(64) NOT NULL COMMENT '设备SN码/序列号',
    brand           VARCHAR(32)  NULL     COMMENT '品牌',
    model           VARCHAR(64)  NULL     COMMENT '型号',
    ip_address      VARCHAR(45)  NULL     COMMENT '内网IP',
    status          TINYINT DEFAULT 0 COMMENT '0:离线, 1:在线, 2:抢票中',
    last_seen       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_sn (sn)
) ENGINE=InnoDB COMMENT='设备管理主表';

-- ========================================================
-- 4. 管理扩展表：设备分组
-- ========================================================
CREATE TABLE IF NOT EXISTS device_groups (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(64) NOT NULL UNIQUE COMMENT '组名',
    config_json     JSON NULL COMMENT '该组特有的配置(延迟、策略等)',
    description     VARCHAR(255) NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='设备分组逻辑表';

-- ========================================================
-- 5. 关联表：设备-分组映射
-- ========================================================
CREATE TABLE IF NOT EXISTS device_group_link (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    device_sn       VARCHAR(64) NOT NULL COMMENT '逻辑关联 devices.sn',
    group_id        INT NOT NULL         COMMENT '逻辑关联 device_groups.id',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_sn_group (device_sn, group_id)
) ENGINE=InnoDB COMMENT='设备与分组的多对多关联表';

-- ========================================================
-- 6. 监控预警：行为日志表
-- 记录数百台设备在执行 Frida 脚本、ADB 指令或 Web 请求时的详细过程
-- ========================================================
CREATE TABLE IF NOT EXISTS action_logs (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志自增主键',
    device_sn       VARCHAR(64)  NULL COMMENT '关联设备的序列号(SN)',
    task_id         INT          NULL COMMENT '关联的订单任务ID',
    level           VARCHAR(10)  DEFAULT 'INFO' COMMENT '日志级别: DEBUG/INFO/WARNING/ERROR',
    module          VARCHAR(32)  NULL COMMENT '所属模块: Frida(脚本)/ADB(指令)/Web(上报)/System(系统)',
    content         TEXT         NULL COMMENT '详细日志内容或报错堆栈',
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '记录产生时间',

    INDEX idx_device_sn (device_sn) COMMENT '设备快速检索索引',
    INDEX idx_created_at (created_at) COMMENT '时间筛选索引',
    INDEX idx_level (level) COMMENT '级别过滤索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备执行行为日志明细表';


CREATE TABLE IF NOT EXISTS `order_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(64) NOT NULL COMMENT '城市',
  `artist` varchar(128) NOT NULL COMMENT '艺人/演出名称',
  `target_date` date DEFAULT NULL COMMENT '目标日期',
  `target_price` decimal(10,2) DEFAULT NULL COMMENT '目标票价',
  `customer_info` varchar(500) DEFAULT NULL COMMENT '实名人信息(姓名+身份证)',
  `priority_order` varchar(255) DEFAULT NULL COMMENT '优先顺序',
  `bounty` decimal(10,2) DEFAULT NULL COMMENT '红包金额',
  `contact_phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `status` tinyint DEFAULT '0' COMMENT '状态: 0待处理, 1已抢到, 2已撤单',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_artist_customer` (`artist`, `customer_info`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE  IF NOT EXISTS `ticket_items` (
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
  KEY `idx_sale_time` (`sale_start_time`),
  KEY `idx_price_time` (`price`,`perform_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 ;
create table tickets.order_tasks
(
    id             int auto_increment
        primary key,
    city           varchar(64)       not null comment '城市',
    artist         varchar(128)      not null comment '艺人/演出名称',
    target_date    date              null comment '目标日期',
    target_price   decimal(10, 2)    null comment '目标票价',
    customer_info  varchar(500)      null comment '实名人信息(姓名+身份证)',
    priority_order varchar(255)      null comment '优先顺序',
    bounty         decimal(10, 2)    null comment '红包金额',
    contact_phone  varchar(20)       null comment '联系电话',
    status         tinyint default 0 null comment '状态: 0待处理, 1已抢到, 2已撤单',
    created_at     datetime          null comment '创建时间',
    constraint uk_artist_customer
        unique (artist, customer_info)
);

create index idx_status
    on tickets.order_tasks (status);

create table tickets.ticket_items
(
    id              bigint auto_increment
        primary key,
    item_id         varchar(32)          not null comment '项目ID',
    project_title   varchar(255)         null comment '演出名称',
    venue_name      varchar(128)         null comment '场馆',
    perform_id      varchar(32)          not null comment '场次ID',
    perform_time    datetime             null comment '演出时间',
    sku_id          varchar(32)          not null comment '票档SKU ID',
    price_name      varchar(64)          null comment '票档描述',
    price           decimal(10, 2)       null comment '价格',
    stock_status    tinyint(1) default 1 null comment '是否有票: 1有, 0无',
    limit_quantity  int        default 4 null comment '每单限购额',
    sale_start_time datetime             null comment '开抢时间',
    updated_at      datetime             null,
    constraint sku_id
        unique (sku_id)
);

create index idx_perform_sku
    on tickets.ticket_items (perform_id, sku_id);

create index idx_price_time
    on tickets.ticket_items (price, perform_time);

create index idx_sale_time
    on tickets.ticket_items (sale_start_time);


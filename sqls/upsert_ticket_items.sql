INSERT INTO `ticket_items` (
    item_id, project_title, venue_name, perform_id, perform_time,
    sku_id, price_name, price, stock_status, limit_quantity,
    sale_start_time, updated_at
) VALUES (
    %(item_id)s, %(project_title)s, %(venue_name)s, %(perform_id)s, %(perform_time)s,
    %(sku_id)s, %(price_name)s, %(price)s, %(stock_status)s, %(limit_quantity)s,
    %(sale_start_time)s, %(updated_at)s
)
ON DUPLICATE KEY UPDATE
    stock_status = VALUES(stock_status),
    price        = VALUES(price),
    updated_at   = VALUES(updated_at);
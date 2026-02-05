SELECT
    t.id AS task_id,
    t.bounty AS bounty,
    t.customer_info AS customer,
    t.priority_order AS priority_order,
    t.artist AS artist,
    t.target_price AS target_price,
    i.project_title AS project_full_name,
    i.price_name AS price_tag,
    i.item_id AS item_id,
    i.sku_id AS sku_id,
    i.perform_id AS perform_id,
    i.stock_status AS has_stock
FROM order_tasks t
INNER JOIN ticket_items i ON (
    i.project_title LIKE CONCAT('%', t.artist, '%')
    AND i.perform_time >= t.target_date
    AND i.perform_time < DATE_ADD(t.target_date, INTERVAL 1 DAY)
    AND i.price = t.target_price
)
WHERE t.status = 0
-- 动态条件将在 Python 中拼接或作为可选占位符处理
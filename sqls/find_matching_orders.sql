SELECT customer_info, bounty, contact_phone
FROM order_tasks
WHERE %(project_title)s LIKE CONCAT('%', artist, '%')
  AND %(price_name)s LIKE CONCAT('%', CAST(target_price AS CHAR), '%')
  AND status = 0
ORDER BY bounty DESC;
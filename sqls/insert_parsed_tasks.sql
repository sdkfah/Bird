INSERT INTO `order_tasks` (
    city, artist, target_date, target_price, customer_info,
    priority_order, bounty, contact_phone, created_at
) VALUES (
    %(city)s, %(artist)s, %(date)s, %(price)s, %(info)s,
    %(priority)s, %(bounty)s, %(phone)s, %(created_at)s
)
ON DUPLICATE KEY UPDATE
    bounty = VALUES(bounty),
    contact_phone = VALUES(contact_phone),
    target_price = VALUES(target_price),
    status = 0;
SELECT DATE(order_date) AS order_day,
    SUM(order_total) AS revenue
FROM orders_transformed
GROUP BY order_day
ORDER BY order_day;
SELECT product_id,
    SUM(qty) AS units_sold,
    SUM(order_total) AS revenue
FROM orders_transformed
GROUP BY product_id
ORDER BY revenue DESC;
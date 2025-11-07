SELECT product_id,
    SUM(stock) AS stock
FROM inventory
GROUP BY product_id
HAVING SUM(stock) < 10
ORDER BY stock ASC;
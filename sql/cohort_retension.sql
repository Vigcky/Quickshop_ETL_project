WITH first_order AS (
    SELECT customer_id,
        MIN(DATE(order_date)) AS cohort_date
    FROM orders_transformed
    GROUP BY customer_id
),
activity AS (
    SELECT f.customer_id,
        f.cohort_date,
        DATE(o.order_date) AS order_day
    FROM first_order f
        JOIN orders_transformed o USING (customer_id)
)
SELECT cohort_date,
    order_day,
    COUNT(DISTINCT customer_id) AS customers
FROM activity
GROUP BY cohort_date,
    order_day
ORDER BY cohort_date,
    order_day;
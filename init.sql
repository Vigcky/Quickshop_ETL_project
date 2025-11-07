CREATE TABLE orders_transformed (
    order_id SERIAL PRIMARY KEY,
    product_id INT,
    qty INT,
    unit_price NUMERIC(10, 2),
    order_total NUMERIC(10, 2),
    order_date DATE
);
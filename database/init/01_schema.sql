DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    segment VARCHAR(50) NOT NULL
);
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL
);
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);
INSERT INTO customers (customer_name, region, segment) VALUES
('Acme Corp', 'South', 'Enterprise'),
('Bright Retail', 'West', 'SMB'),
('NextGen Stores', 'East', 'Enterprise'),
('UrbanMart', 'North', 'SMB'),
('ValuePoint', 'South', 'Mid-Market'),
('QuickBuy', 'West', 'SMB');
INSERT INTO products (product_name, category, unit_price) VALUES
('Wireless Mouse', 'Electronics', 25.00),
('Mechanical Keyboard', 'Electronics', 85.00),
('Office Chair', 'Furniture', 150.00),
('Standing Desk', 'Furniture', 320.00),
('Notebook Pack', 'Stationery', 12.00),
('Desk Lamp', 'Furniture', 45.00),
('USB-C Hub', 'Electronics', 60.00),
('Whiteboard Markers', 'Stationery', 10.00);
INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2025-01-10', 'Completed'),
(2, '2025-01-15', 'Completed'),
(3, '2025-02-03', 'Completed'),
(4, '2025-02-18', 'Cancelled'),
(5, '2025-03-01', 'Completed'),
(6, '2025-03-12', 'Completed'),
(1, '2025-04-05', 'Completed'),
(3, '2025-04-20', 'Completed'),
(2, '2025-05-08', 'Completed'),
(5, '2025-05-22', 'Pending');
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 10, 25.00),
(1, 2, 5, 85.00),
(2, 5, 20, 12.00),
(2, 8, 15, 10.00),
(3, 3, 4, 150.00),
(3, 4, 2, 320.00),
(4, 7, 3, 60.00),
(5, 6, 8, 45.00),
(5, 1, 6, 25.00),
(6, 2, 7, 85.00),
(6, 7, 5, 60.00),
(7, 4, 3, 320.00),
(7, 3, 2, 150.00),
(8, 1, 12, 25.00),
(8, 5, 30, 12.00),
(9, 6, 10, 45.00),
(9, 8, 25, 10.00),
(10, 2, 4, 85.00);
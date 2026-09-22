CREATE DATABASE IF NOT EXISTS ai_sales;
USE ai_sales;

-- ============================================
-- CUSTOMERS
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    city VARCHAR(100),
    registration_date DATE
);

-- ============================================
-- PRODUCTS
-- ============================================
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2)
);

-- ============================================
-- ORDERS
-- ============================================
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ============================================
-- CUSTOMERS DATA
-- ============================================
INSERT INTO customers (name, email, city, registration_date) VALUES
('Rahul Sharma', 'rahul@gmail.com', 'Mumbai', '2025-01-10'),
('Priya Patil', 'priya@gmail.com', 'Pune', '2025-02-15'),
('Amit Kumar', 'amit@gmail.com', 'Delhi', '2025-03-20'),
('Sneha Joshi', 'sneha@gmail.com', 'Nagpur', '2025-04-12'),
('Rohit Verma', 'rohit@gmail.com', 'Bangalore', '2025-05-18'),
('Neha Singh', 'neha@gmail.com', 'Hyderabad', '2025-06-22'),
('Vikas More', 'vikas@gmail.com', 'Nashik', '2025-07-05'),
('Pooja Deshmukh', 'pooja@gmail.com', 'Amravati', '2025-07-18');

-- ============================================
-- PRODUCTS DATA
-- ============================================
INSERT INTO products (product_name, category, price) VALUES
('Laptop', 'Electronics', 65000),
('Mobile Phone', 'Electronics', 30000),
('Keyboard', 'Accessories', 2500),
('Mouse', 'Accessories', 1200),
('Monitor', 'Electronics', 18000),
('Headphones', 'Accessories', 3500),
('Tablet', 'Electronics', 25000),
('Webcam', 'Accessories', 4500);

-- ============================================
-- ORDERS DATA
-- ============================================
INSERT INTO orders (customer_id, product_id, quantity, order_date, amount) VALUES
(1, 1, 1, '2025-08-01', 65000),
(1, 3, 2, '2025-08-05', 5000),
(2, 2, 1, '2025-08-07', 30000),
(2, 6, 1, '2025-08-12', 3500),
(3, 5, 2, '2025-08-15', 36000),
(3, 4, 2, '2025-08-17', 2400),
(4, 7, 1, '2025-08-20', 25000),
(4, 8, 1, '2025-08-22', 4500),
(5, 1, 2, '2025-08-25', 130000),
(5, 6, 2, '2025-08-27', 7000),
(6, 2, 2, '2025-08-28', 60000),
(7, 5, 1, '2025-08-29', 18000),
(7, 3, 3, '2025-08-30', 7500),
(8, 7, 2, '2025-08-31', 50000);

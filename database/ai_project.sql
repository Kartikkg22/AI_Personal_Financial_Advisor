CREATE DATABASE financial_advisor;

USE financial_advisor;

-- table creations required in the project
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Store hashed passwords
    income DECIMAL(15, 2) DEFAULT 0.00,
    expenses DECIMAL(15, 2) DEFAULT 0.00,
    savings DECIMAL(15, 2) DEFAULT 0.00,
    goals TEXT,  -- JSON or text to store financial goals
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    category VARCHAR(50),  -- Expense category (e.g., housing, food)
    transaction_type ENUM('income', 'expense') NOT NULL,  -- Whether it's an income or expense
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    budget_limit DECIMAL(15, 2) NOT NULL,
    current_spending DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE financial_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goal_name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(15, 2) NOT NULL,
    current_amount DECIMAL(15, 2) DEFAULT 0.00,
    goal_type ENUM('short_term', 'long_term') NOT NULL,  -- Short-term or long-term goals
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE investment_portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    investment_type VARCHAR(50),  -- e.g., stocks, bonds, mutual funds
    asset_name VARCHAR(100),  -- The name of the stock, fund, etc.
    amount DECIMAL(15, 2) NOT NULL,  -- The amount invested
    date_of_investment DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tax_information (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    taxable_income DECIMAL(15, 2) NOT NULL,  -- The amount of income subject to tax
    tax_deductions DECIMAL(15, 2) DEFAULT 0.00,  -- Deductions the user is eligible for
    tax_exemptions DECIMAL(15, 2) DEFAULT 0.00,  -- Exemptions user can claim
    tax_paid DECIMAL(15, 2) DEFAULT 0.00,  -- Tax already paid
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE market_insights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- sample inputs for the project
INSERT INTO users (name, email, password_hash, income, expenses, savings, goals) 
VALUES 
('John Doe', 'john.doe@example.com', 'hashedpassword123', 5000.00, 2500.00, 1000.00, '{"retirement": "500000", "vacation": "10000"}'),
('Jane Smith', 'jane.smith@example.com', 'hashedpassword456', 7000.00, 3000.00, 2000.00, '{"house": "100000", "education": "20000"}');
INSERT INTO transactions (user_id, amount, category, transaction_type, date) 
VALUES 
(1, 1500.00, 'housing', 'expense', '2024-11-01'),
(1, 800.00, 'food', 'expense', '2024-11-05'),
(1, 1200.00, 'salary', 'income', '2024-11-01'),
(2, 2500.00, 'salary', 'income', '2024-11-02'),
(2, 1000.00, 'shopping', 'expense', '2024-11-10');
INSERT INTO financial_goals (user_id, goal_name, target_amount, current_amount, goal_type, target_date) 
VALUES 
(1, 'Retirement Savings', 500000.00, 10000.00, 'long_term', '2050-12-31'),
(1, 'Vacation Fund', 10000.00, 2000.00, 'short_term', '2025-06-30'),
(2, 'House Down Payment', 100000.00, 50000.00, 'long_term', '2030-01-01');
INSERT INTO budgets (user_id, category, budget_limit, current_spending) 
VALUES 
(1, 'housing', 2000.00, 1500.00),
(1, 'food', 1000.00, 800.00),
(2, 'shopping', 1500.00, 1000.00);
INSERT INTO investment_portfolio (user_id, investment_type, asset_name, amount, date_of_investment) 
VALUES 
(1, 'stocks', 'Apple Inc.', 1500.00, '2024-01-15'),
(1, 'mutual fund', 'Bluechip Fund', 2000.00, '2024-03-01'),
(2, 'bonds', 'Government Bond', 5000.00, '2023-12-01');
INSERT INTO tax_information (user_id, taxable_income, tax_deductions, tax_exemptions, tax_paid) 
VALUES 
(1, 3000.00, 500.00, 200.00, 300.00),
(2, 7000.00, 1000.00, 500.00, 800.00);
INSERT INTO market_insights (title, content, date) 
VALUES 
('Stock Market Boom', 'The stock market has reached an all-time high.', '2024-11-01'),
('Housing Market Trends', 'Home prices are expected to rise in the next quarter.', '2024-10-15'),
('Investment Tips', 'Diversify your portfolio to reduce risk.', '2024-11-05');

SELECT 
    u.name, 
    u.email, 
    u.income, 
    u.expenses, 
    u.savings, 
    u.goals,
    SUM(t.amount) AS total_transactions,
    GROUP_CONCAT(DISTINCT b.category) AS budget_categories,
    GROUP_CONCAT(DISTINCT f.goal_name) AS financial_goals
FROM 
    users u
LEFT JOIN 
    transactions t ON u.id = t.user_id
LEFT JOIN 
    budgets b ON u.id = b.user_id
LEFT JOIN 
    financial_goals f ON u.id = f.user_id
WHERE 
    u.id = 1
GROUP BY 
    u.id;

ALTER TABLE users
ADD COLUMN account_status ENUM('active', 'inactive') DEFAULT 'active';

CREATE TABLE price_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    target_price DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

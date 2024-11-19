USE ai_project;

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
VALUES ('Jane Smith', 'jane.smith@example.com', 'hashed_password_here', 75000.00, 25000.00, 15000.00, '{"retirement": 200000.00, "house": 300000.00}');

INSERT INTO transactions (user_id, amount, category, transaction_type) 
VALUES (1, 500.00, 'food', 'expense');

INSERT INTO budgets (user_id, category, budget_limit, current_spending) 
VALUES (1, 'housing', 25000.00, 2000.00);

INSERT INTO financial_goals (user_id, goal_name, target_amount, current_amount, goal_type, target_date) 
VALUES (1, 'Retirement Fund', 200000.00, 30000.00, 'long_term', '2040-12-31');

select * from users
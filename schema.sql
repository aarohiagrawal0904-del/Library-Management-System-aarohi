CREATE DATABASE IF NOT EXISTS library_system;
USE library_system;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    quantity INT DEFAULT 1,
    available_quantity INT DEFAULT 1,
    cover_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    return_date TIMESTAMP NULL,
    status ENUM('issued', 'returned') DEFAULT 'issued',
    fine DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Default Admin User (Password: admin123)
-- Hash generated using Python's werkzeug.security.generate_password_hash OR compatible method
-- You might need to update this hash if you change the hashing method in Python code.
-- For this schema, we will insert a placeholder. The Python app should handle registration/seeding better.
INSERT INTO users (username, email, password_hash, role) 
SELECT 'admin', 'admin@library.com', 'scrypt:32768:8:1$kPz...', 'admin' 
WHERE NOT EXISTS (SELECT * FROM users WHERE email = 'admin@library.com');

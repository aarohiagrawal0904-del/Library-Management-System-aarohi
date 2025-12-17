# Library Management System

A beginner-friendly, clean, and modern Library Management System built with **Python (Flask)** and **MySQL**.

## Features

- **User Authentication**: Secure login and registration for Students and Admins.
- **Admin Dashboard**:
  - Manage Books (Add, Edit, Delete, View).
  - Issue Books to students.
  - Return Books with Fine calculation (overdue handling).
  - View Issue History.
- **Student Dashboard**:
  - View currently issued books and due dates.
  - Browse available books in the library.
- **Security**: Uses `Werkzeug` for password hashing and `Flask-Login` for session management.
- **UI**: Premium Glassmorphism design using CSS variables and modern layout.

## Folder Structure

```
/app
    /static
        /css        - Stylesheets (Modern Glassmorphism)
        /js         - Scripts
    /templates      - HTML Templates (Jinja2)
    __init__.py     - App factory
    models.py       - Database models
    routes_*.py     - Route controllers
/legacy_php        - Old PHP version code
config.py          - App configuration
run.py             - Entry point
schema.sql         - Database schema
requirements.txt   - Python dependencies
```

## Setup Instructions

### 1. Database Setup
1.  Install **MySQL** if you haven't already.
2.  Create a database named `library_system`.
3.  Execute the script in `schema.sql` to create tables and default admin.
    -   You can use MySQL Workbench or command line:
        ```bash
        mysql -u root -p < schema.sql
        ```
    -   **Note**: The default admin password hash in `schema.sql` is a placeholder. You may need to create a new admin via the register page or update the hash manually.
    -   *Easiest way*: Go to `/register`, create an account, select "Admin" role (available for demo purposes).

### 2. Python Setup
1.  Install Python (3.8+).
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration
1.  Open `config.py`.
2.  Update the `DB_USER` and `DB_PASSWORD` fields to match your local MySQL credentials.
    ```python
    DB_USER = 'root'
    DB_PASSWORD = 'your_password'
    ```

### 4. Run to Project
1.  Run the application:
    ```bash
    python run.py
    ```
2.  Open your browser and navigate to:
    `http://127.0.0.1:5000`

## Tech Stack
-   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript
-   **Backend**: Python (Flask)
-   **Database**: MySQL
-   **ORM**: SQLAlchemy

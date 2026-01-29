# Database Setup Guide

This guide will help you set up your MySQL database for the Redback Hiring application.

## Prerequisites

- MySQL Server installed on your system
- Your `.env` file configured with database credentials (see `.env` file)

## Step 1: Start MySQL Server

### On Linux (Ubuntu/Debian)
```bash
sudo systemctl start mysql
```

### On macOS with Homebrew
```bash
brew services start mysql
```

### Verify MySQL is Running
```bash
sudo systemctl status mysql
# or on macOS:
# brew services list
```

## Step 2: Create the Database and User

Log into MySQL with root privileges:

```bash
```

**Note:** If root has no password, just press Enter when prompted.

Once logged in, run the following commands:

```sql
-- Create the interview database
CREATE DATABASE interview;

-- Create the ravi user (as configured in .env)
CREATE USER 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234';

-- Grant all privileges on the interview database to ravi user
GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

## Step 3: Initialize the Database Schema

Navigate to your project directory and run the database initialization script:

```bash
cd /home/kantdravi/Desktop/project_hire/redback_hiring/hire
```

Run this command to create all necessary tables:

```bash
python3 -c "from app import create_app; from models.db import db
app = create_app()
with app.app_context():
    db.create_all()
    print('✓ Database initialized successfully')"
```

## Step 4: Start Your Application

Once the database is initialized, start your application:

```bash
python3 app.py
```

Your application should now be running and connected to the MySQL database.

## Troubleshooting

### MySQL Connection Refused
- Ensure MySQL is running: `sudo systemctl status mysql`
- Check if port 3306 is accessible
- Verify credentials in `.env` file

### Access Denied for User 'ravi'@'localhost'
- Ensure the user was created with the correct password
- Try logging in directly: `mysql -u ravi -p` (password: `Ravi@1234`)

### Database Not Found
- Confirm the `interview` database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Re-run the CREATE DATABASE command if needed

## Environment Variables

Your `.env` file should contain:

```dotenv
MYSQL_USER=ravi
MYSQL_PASSWORD=Ravi@1234
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=interview
SECRET_KEY=dev-secret-key-change-in-production
```

## Resetting the Database

If you need to completely reset and start fresh:

```bash
mysql -u root -p -e "DROP DATABASE interview;"
```

Then follow Steps 2-3 again to recreate the database.

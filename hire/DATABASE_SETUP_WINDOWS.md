# Database Setup Guide for Windows

This guide will help you set up your MySQL database for the Redback Hiring application on Windows.

## Prerequisites

- MySQL Server installed on your Windows system
- Your `.env` file configured with database credentials (see `.env` file)
- Command Prompt or PowerShell with administrator privileges

## Step 1: Start MySQL Server on Windows

### Option 1: Using Services (Recommended)
1. Press `Win + R` to open the Run dialog
2. Type `services.msc` and press Enter
3. Find **MySQL** (or **MySQL80** depending on your version) in the list
4. Right-click on it and select **Start**

### Option 2: Using Command Prompt
Open Command Prompt as Administrator and run:

```cmd
net start MySQL80
```

**Note:** Replace `MySQL80` with your MySQL version if different (e.g., `MySQL57`, `MySQL81`)

### Option 3: Using MySQL Shell
Open Command Prompt or PowerShell and run:

```cmd
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld" --console
```

**Note:** Adjust the path based on your MySQL installation directory.

### Verify MySQL is Running
Check if MySQL is running by trying to connect:

```cmd
mysql -u root -p
```

If you see the MySQL prompt (`mysql>`), it's running successfully. Type `EXIT;` to close.

## Step 2: Create the Database and User

Open Command Prompt or PowerShell and log into MySQL with root:

```cmd
mysql -u root -p
```

When prompted, enter your root password (or press Enter if no password is set).

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

Open Command Prompt or PowerShell and navigate to your project directory:

```cmd
cd "C:\Users\YourUsername\Desktop\project_hire\redback_hiring\hire"
```

Run this command to create all necessary tables:

```cmd
python3 -c "from models.db import db; from app import app; with app.app_context(): db.create_all(); print('✓ Database initialized successfully')"
```

Or as a single line:

```cmd
python3 -c "from models.db import db; from app import app; with app.app_context(): db.create_all(); print('Database initialized successfully')"
```

## Step 4: Start Your Application

Once the database is initialized, start your application:

```cmd
python3 app.py
```

Your application should now be running and connected to the MySQL database. Open your browser and navigate to `http://localhost:5000` (or the port shown in terminal).

## Troubleshooting

### MySQL Service Won't Start
1. Open Services (Win + R → `services.msc`)
2. Right-click MySQL service → Properties
3. Check the "Path to executable" is correct
4. Try restarting your computer and starting the service again

### Access Denied for User 'ravi'@'localhost'
1. Verify credentials in `.env` file
2. Try logging in directly: `mysql -u ravi -p` (password: `Ravi@1234`)
3. If it fails, drop and recreate the user:
   ```sql
   DROP USER 'ravi'@'localhost';
   CREATE USER 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234';
   GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Python Connection Error
- Ensure MySQL is running (check Services)
- Verify port 3306 is not blocked by Windows Firewall
- Check that all `.env` credentials are correct
- Install required Python package: `pip install pymysql`

### Database Not Found
- Verify the database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- If missing, log in and run: `CREATE DATABASE interview;`

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

```cmd
mysql -u root -p -e "DROP DATABASE interview;"
```

Then follow Steps 2-3 again to recreate the database.

## Alternative: Using MySQL Workbench (GUI)

If you prefer a graphical interface:

1. Open **MySQL Workbench**
2. Connect to your local MySQL server
3. In the SQL Editor, create the database and user using the SQL commands from Step 2
4. Continue with Step 3

## Finding Your MySQL Installation Path

If you need to locate MySQL:

```cmd
where mysql
```

This will show you the path to mysql.exe on your system.

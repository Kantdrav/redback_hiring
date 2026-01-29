# Database Setup Guide using MySQL Workbench

This guide will help you set up your MySQL database using MySQL Workbench's graphical interface for the Redback Hiring application.

## Prerequisites

- MySQL Server installed and running
- MySQL Workbench installed on your system
- Your `.env` file configured with database credentials

## Step 1: Open MySQL Workbench

1. Launch **MySQL Workbench**
2. You should see your local MySQL connection (usually named "Local instance MySQL80" or similar)
3. Click on the connection to open it
4. Enter your MySQL root password if prompted

## Step 2: Create the Database

1. In the left sidebar, right-click on **Schemas**
2. Select **Create Schema...**
3. In the dialog box that appears:
   - **Name:** Type `interview`
   - **Charset:** Leave as default (utf8mb4)
   - **Collation:** Leave as default
4. Click **Apply**
5. Click **Apply** again in the confirmation dialog
6. Click **Finish**

You should now see the `interview` database listed under Schemas.

## Step 3: Create the Database User

1. In the left sidebar, go to **Administration** tab (you may need to click on it at the bottom)
2. Click on **Users and Privileges**
3. Click the **Add Account** button

### User Configuration:

**Login Name Tab:**
- **Login Name:** `ravi`
- **Limit to Hosts Matching:** `localhost`

**Authentication Type Tab:**
- **Password:** `Ravi@1234`
- **Confirm Password:** `Ravi@1234`
- **Default Schema:** `interview`

### Grant Privileges:

1. Still in the Users and Privileges window, click on the **Schema Privileges** tab
2. Click **Add Entry** button
3. In the dialog, select:
   - **Schema:** `interview`
   - Click **OK**
4. Now you should see `interview.*` listed
5. In the **Privileges** section, check the following boxes:
   - ✓ ALL (this will select all privileges automatically)
   
   Or manually select:
   - ✓ SELECT
   - ✓ INSERT
   - ✓ UPDATE
   - ✓ DELETE
   - ✓ CREATE
   - ✓ DROP
   - ✓ GRANT
   - ✓ ALTER
   - ✓ CREATE TEMPORARY TABLES
   - ✓ LOCK TABLES
   - ✓ CREATE VIEW
   - ✓ SHOW VIEW
   - ✓ CREATE ROUTINE
   - ✓ ALTER ROUTINE
   - ✓ TRIGGER

6. Click **Apply Changes** button
7. Click **Finish**

### Verify User Creation:

Back in the Users and Privileges window, you should see:
- User: `ravi@localhost`
- Default Schema: `interview`

## Step 4: Test the Connection (Optional but Recommended)

### Create a New MySQL Connection:

1. Click the **+** button next to the connection tabs at the top
2. Fill in the following details:
   - **Connection Name:** `Hiring App Local`
   - **Connection Method:** Standard (TCP/IP)
   - **Hostname:** `localhost`
   - **Port:** `3306`
   - **Username:** `ravi`
   - **Password:** `Ravi@1234`
   - **Default Schema:** `interview`

3. Click **Test Connection**
4. You should see "Connection successful"
5. Click **OK**

This tests that the `ravi` user can connect properly.

## Step 5: Initialize the Database Schema (Python)

Now you need to run the Python initialization script to create the database tables.

Open a terminal and navigate to your project directory:

```bash
cd /home/kantdravi/Desktop/project_hire/redback_hiring/hire
```

Run the initialization command:

```bash
python3 -c "from app import create_app; from models.db import db
app = create_app()
with app.app_context():
    db.create_all()
    print('✓ Database initialized successfully')"
```

Or simply run:

```bash
python3 app.py
```

## Step 6: Verify Database Tables in Workbench

1. In MySQL Workbench, go to the **Schemas** tab in the left sidebar
2. Expand the `interview` database
3. Expand **Tables**
4. You should see all the database tables created by your application

### Common tables you should see:
- `user`
- `admin_logs`
- `website_visit`
- `job`
- `candidate`
- `interview`
- `assessment`
- `round`
- And others depending on your models

## Step 7: Start Your Application

Once verified, start your Flask application:

```bash
python3 app.py
```

Your application should now be running on `http://localhost:5000`

## Common Workbench Tasks

### View Database Tables

1. In Schemas panel, expand `interview` → **Tables**
2. Right-click on any table and select **Select Rows**
3. You can view and edit data directly in the workbench

### Execute SQL Queries

1. Click **File** → **New Query Tab** or use the SQL editor icon
2. Type your SQL query
3. Click the lightning bolt icon or press Ctrl+Enter to execute

### Example Query - View All Users:

```sql
SELECT * FROM interview.user;
```

### Backup Your Database

1. Right-click on `interview` schema
2. Select **Data Export**
3. Choose export options and destination
4. Click **Start Export**

### Reset Database

If you need to reset everything:

1. Right-click on `interview` schema
2. Select **Drop Schema...**
3. Confirm the deletion
4. Follow Steps 2-5 again to recreate

## Troubleshooting in Workbench

### Cannot Connect to Server
- Click the connection and check the connection parameters
- Verify MySQL Server is running: Look for green status indicator
- Check username and password are correct

### Schema Appears Empty After Python Initialization
- Click **Refresh** in the schemas panel (right-click or use F5)
- Expand Tables again to see the newly created tables

### Privileges Not Applied
- In Users and Privileges, click **Refresh** button
- Log out and log back in to the connection
- Try creating a new connection with the `ravi` user to test permissions

## Next Steps

Once your database is set up:

1. Create an admin user (if not already done):
   ```bash
   python3 create_admin.py
   ```

2. Start the application:
   ```bash
   python3 app.py
   ```

3. Access the web application at `http://localhost:5000`

## Environment Variables Reference

Your `.env` file should contain:

```dotenv
MYSQL_USER=ravi
MYSQL_PASSWORD=Ravi@1234
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=interview
SECRET_KEY=dev-secret-key-change-in-production
```

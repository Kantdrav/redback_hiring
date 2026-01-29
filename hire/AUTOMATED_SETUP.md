# Automated Database Setup

I've created automated scripts to set up your entire database in one command!

## Quick Start

### Option 1: Python Script (Recommended - Cross-platform)

```bash
python3 setup_database.py
```

This script will:
1. ✓ Check if MySQL is installed
2. ✓ Check if MySQL server is running (start it if needed)
3. ✓ Create the `interview` database
4. ✓ Create the `ravi` user with password `Ravi@1234`
5. ✓ Grant all necessary privileges
6. ✓ Initialize database schema (create all tables)
7. ✓ Verify the setup

### Option 2: Shell Script (Linux/macOS)

Make it executable first:
```bash
chmod +x setup_database.sh
```

Then run it:
```bash
./setup_database.sh
```

Same functionality as the Python script above.

### Option 3: Windows Batch Script

```batch
setup_database.bat
```

## What Each Script Does

### setup_database.py
- **Language:** Python 3
- **Requirements:** Python 3.6+, MySQL, sudo access
- **Benefits:** Works on Linux, macOS, and Windows (with Python)
- **Pros:** Better error handling, colored output, detailed feedback

### setup_database.sh
- **Language:** Bash
- **Requirements:** Bash shell, MySQL, sudo access
- **Best for:** Linux and macOS users
- **Speed:** Slightly faster than Python version

## After Successful Setup

Once the script completes successfully, you'll see:

```
============================================================
   ✓ Database setup completed successfully!
============================================================

Database: interview
User: ravi
Host: localhost

Next steps:
1. Create admin user: python3 create_admin.py
2. Start the application: python3 app.py
3. Open browser: http://localhost:5000
```

Then follow these steps:

### Step 1: Create Admin User
```bash
python3 create_admin.py
```

Follow the prompts to create your admin account.

### Step 2: Start the Application
```bash
python3 app.py
```

### Step 3: Access the Application
Open your browser and go to:
```
http://localhost:5000
```

## Troubleshooting

### Script Says MySQL is Not Running
- **Linux:** Run `sudo systemctl start mysql`
- **macOS:** Run `brew services start mysql`
- **Windows:** Start MySQL from Services or command line

### Access Denied Error
This usually means:
- MySQL root user doesn't have a password set (try without `-p` flag)
- Or you need to enter MySQL password when prompted

### Database Already Exists
- The scripts use `CREATE DATABASE IF NOT EXISTS`
- So they won't error if database already exists
- Old data will be preserved

### Permission Denied on Script
**Linux/macOS:** Make the script executable first:
```bash
chmod +x setup_database.sh
```

## Manual Reset (if needed)

If you need to reset and start fresh:

```bash
# Drop the database
sudo mysql -u root -e "DROP DATABASE interview;"

# Run the setup script again
python3 setup_database.py
```

## Alternative: One-Liner Commands

If you prefer not to use the scripts:

### Linux/macOS:
```bash
sudo mysql -u root -e "CREATE DATABASE interview; CREATE USER 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234'; GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost'; FLUSH PRIVILEGES;" && python3 -c "from app import create_app; from models.db import db; app = create_app(); db.create_all(); print('✓ Setup complete')"
```

### Windows (PowerShell):
```powershell
mysql -u root -e "CREATE DATABASE interview; CREATE USER 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234'; GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost'; FLUSH PRIVILEGES;" ; python3 -c "from app import create_app; from models.db import db; app = create_app(); db.create_all(); print('✓ Setup complete')"
```

## FAQ

**Q: Why does the script need sudo?**
A: Creating users and setting privileges requires root/admin access to MySQL.

**Q: Can I change the password?**
A: Yes, edit the script and replace `Ravi@1234` with your desired password. Also update your `.env` file.

**Q: What if MySQL has a root password?**
A: The scripts assume no root password (default on Linux). If you have one, you'll need to:
1. Modify the scripts to add `-p` flag
2. Or use MySQL Workbench instead

**Q: Does it delete existing data?**
A: No, the scripts use `CREATE IF NOT EXISTS` to avoid overwriting existing databases.

## Files Included

- `setup_database.py` - Python automated setup script
- `setup_database.sh` - Bash shell script for Linux/macOS
- `AUTOMATED_SETUP.md` - This file

Choose the script that best fits your environment!

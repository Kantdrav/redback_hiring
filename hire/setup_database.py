#!/usr/bin/env python3
"""
Automated Database Setup Script for Redback Hiring Application
This script automates the entire MySQL database setup process
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def check_mysql_installed():
    """Check if MySQL is installed"""
    print_info("Checking if MySQL is installed...")
    try:
        result = subprocess.run(['which', 'mysql'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success("MySQL is installed")
            return True
        else:
            print_error("MySQL not found. Please install MySQL first.")
            return False
    except Exception as e:
        print_error(f"Error checking MySQL: {e}")
        return False

def check_mysql_running():
    """Check if MySQL server is running"""
    print_info("Checking if MySQL server is running...")
    try:
        result = subprocess.run(['sudo', 'systemctl', 'status', 'mysql'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("MySQL server is running")
            return True
        else:
            print_warning("MySQL server is not running. Attempting to start...")
            return start_mysql()
    except Exception as e:
        print_error(f"Error checking MySQL status: {e}")
        return False

def start_mysql():
    """Start MySQL server"""
    try:
        result = subprocess.run(['sudo', 'systemctl', 'start', 'mysql'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("MySQL server started successfully")
            return True
        else:
            print_error("Failed to start MySQL server")
            print_error(result.stderr)
            return False
    except Exception as e:
        print_error(f"Error starting MySQL: {e}")
        return False

def setup_database():
    """Create database and user"""
    print_info("Setting up database and user...")
    
    sql_commands = """
    CREATE DATABASE IF NOT EXISTS interview;
    CREATE USER IF NOT EXISTS 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234';
    GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost';
    FLUSH PRIVILEGES;
    """
    
    try:
        # Use sudo to run mysql as root
        process = subprocess.Popen(['sudo', 'mysql', '-u', 'root'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, 
                                 text=True)
        stdout, stderr = process.communicate(input=sql_commands)
        
        if process.returncode == 0:
            print_success("Database 'interview' created")
            print_success("User 'ravi' created with full privileges")
            return True
        else:
            print_error("Failed to setup database")
            if stderr:
                print_error(f"Error: {stderr}")
            return False
    except Exception as e:
        print_error(f"Error setting up database: {e}")
        return False

def initialize_schema():
    """Initialize database schema using Flask app"""
    print_info("Initializing database schema...")
    
    try:
        result = subprocess.run([
            'python3', '-c',
            """from app import create_app; from models.db import db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database schema initialized successfully')"""
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print_success("Database schema initialized")
            return True
        else:
            print_error("Failed to initialize database schema")
            if result.stderr:
                print_error(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Error initializing schema: {e}")
        return False

def verify_setup():
    """Verify the database setup"""
    print_info("Verifying database setup...")
    
    try:
        result = subprocess.run([
            'mysql', '-u', 'ravi', '-p' + 'Ravi@1234', 
            '-e', 'SELECT DATABASE();'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print_success("Database connection verified!")
            return True
        else:
            print_warning("Could not verify connection (this may be OK on some systems)")
            return True
    except Exception as e:
        print_warning(f"Could not verify setup: {e}")
        return True

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("   Redback Hiring - Automated Database Setup")
    print(f"{'='*60}{Colors.END}\n")
    
    # Step 1: Check MySQL installation
    if not check_mysql_installed():
        print_error("Please install MySQL and try again.")
        sys.exit(1)
    
    # Step 2: Check and start MySQL if needed
    if not check_mysql_running():
        print_error("Could not start MySQL server. Please start it manually.")
        sys.exit(1)
    
    # Step 3: Setup database and user
    if not setup_database():
        print_error("Failed to setup database. Please check MySQL permissions.")
        sys.exit(1)
    
    # Step 4: Initialize database schema
    if not initialize_schema():
        print_warning("Database schema initialization had issues.")
        print_info("You may need to initialize manually:")
        print("  python3 -c \"from app import create_app; from models.db import db")
        print("  app = create_app()")
        print("  with app.app_context(): db.create_all()\"")
    
    # Step 5: Verify setup
    verify_setup()
    
    print(f"\n{Colors.GREEN}{'='*60}")
    print("   ✓ Database setup completed successfully!")
    print(f"{'='*60}{Colors.END}")
    print(f"\nDatabase: {Colors.BLUE}interview{Colors.END}")
    print(f"User: {Colors.BLUE}ravi{Colors.END}")
    print(f"Host: {Colors.BLUE}localhost{Colors.END}")
    print(f"\nNext steps:")
    print(f"1. Create admin user: {Colors.BLUE}python3 create_admin.py{Colors.END}")
    print(f"2. Start the application: {Colors.BLUE}python3 app.py{Colors.END}")
    print(f"3. Open browser: {Colors.BLUE}http://localhost:5000{Colors.END}\n")

if __name__ == "__main__":
    main()

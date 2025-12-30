#!/usr/bin/env python3
"""
Migration script to add experience_years column to candidates table
Run: python migrate_add_experience.py
"""
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL connection imports
import pymysql

def migrate():
    try:
        # Get MySQL credentials from environment
        mysql_user = os.environ.get("MYSQL_USER", "root")
        mysql_password = os.environ.get("MYSQL_PASSWORD", "")
        mysql_host = os.environ.get("MYSQL_HOST", "localhost")
        mysql_port = int(os.environ.get("MYSQL_PORT", "3306"))
        mysql_db = os.environ.get("MYSQL_DB", "interviewflow")
        
        # Connect to MySQL
        print(f"Connecting to MySQL ({mysql_host}:{mysql_port}/{mysql_db})...")
        connection = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Check if column already exists
        print("Checking if experience_years column exists...")
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='candidates' 
            AND COLUMN_NAME='experience_years'
            AND TABLE_SCHEMA=DATABASE()
        """)
        
        if cursor.fetchone():
            print("✓ experience_years column already exists")
            cursor.close()
            connection.close()
            return
        
        # Add the column
        print("Adding experience_years column to candidates table...")
        cursor.execute("""
            ALTER TABLE candidates 
            ADD COLUMN experience_years FLOAT DEFAULT 0
        """)
        connection.commit()
        print("✓ Successfully added experience_years column")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()


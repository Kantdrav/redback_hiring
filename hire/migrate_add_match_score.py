#!/usr/bin/env python3
"""
Migration script to add match_score column to candidates table
Run this script to update the database schema
"""
import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'interviewflow.sqlite')

def migrate():
    """Add match_score column to candidates table"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(candidates)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'match_score' in columns:
            print("✅ Column 'match_score' already exists in candidates table")
            conn.close()
            return True
        
        # Add the column
        cursor.execute("ALTER TABLE candidates ADD COLUMN match_score INTEGER DEFAULT 0")
        conn.commit()
        
        print("✅ Successfully added 'match_score' column to candidates table")
        
        # Verify
        cursor.execute("PRAGMA table_info(candidates)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"📋 Current columns in candidates table: {', '.join(columns)}")
        
        conn.close()
        return True
        
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print("✅ Column 'match_score' already exists")
            return True
        else:
            print(f"❌ Error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Running database migration...")
    print(f"📁 Database: {DB_PATH}")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
        print("🚀 You can now restart the Flask application")
    else:
        print("\n❌ Migration failed!")

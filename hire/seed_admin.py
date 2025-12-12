#!/usr/bin/env python
"""
Script to seed the database with a default admin user.
Run this once to create the admin account.
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from models import User

def seed_admin():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email="admin@interviewflow.local").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email="admin@interviewflow.local",
            name="Administrator",
            role="admin",
            phone="N/A"
        )
        admin.set_password("admin123")
        
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Admin user created successfully!")
        print("  Email: admin@interviewflow.local")
        print("  Password: admin123")

if __name__ == "__main__":
    seed_admin()

#!/usr/bin/env python3
"""
Create Admin User Script
Run this to create the admin account programmatically
"""
from app import create_app, db
from models import User

def create_admin():
    """Create admin user with predefined credentials"""
    app = create_app()
    
    ADMIN_EMAIL = "admin@redback.local"
    ADMIN_PASSWORD = "Admin@2025"
    ADMIN_NAME = "Redback Administrator"
    
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        
        if admin:
            print("⚠️  Admin user already exists!")
            print(f"   Email: {admin.email}")
            print(f"   Name: {admin.name}")
            print(f"   Role: {admin.role}")
            
            # Update password
            response = input("\n🔄 Update admin password? (y/n): ")
            if response.lower() == 'y':
                admin.set_password(ADMIN_PASSWORD)
                db.session.commit()
                print("✅ Admin password updated!")
        else:
            # Create new admin
            admin = User(
                email=ADMIN_EMAIL,
                name=ADMIN_NAME,
                role="admin"
            )
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
        
        print("\n" + "="*60)
        print("🔐 ADMIN LOGIN CREDENTIALS")
        print("="*60)
        print(f"Email:    {ADMIN_EMAIL}")
        print(f"Password: {ADMIN_PASSWORD}")
        print(f"Token:    admin-access-token-2025")
        print("="*60)
        print("\n📝 HOW TO LOGIN AS ADMIN:")
        print("1. Go to: http://localhost:5000/auth/login")
        print("2. Select Role: Admin")
        print("3. Enter Email: admin@redback.local")
        print("4. Enter Password: Admin@2025")
        print("5. Enter Admin Token: admin-access-token-2025")
        print("6. Click Login")
        print("\n⚠️  SECURITY NOTE:")
        print("   - Change the default password after first login")
        print("   - Keep the admin token secure")
        print("   - Both email/password AND token are required for admin login")
        print("="*60)

if __name__ == "__main__":
    print("🚀 Creating Admin User for Redback...\n")
    create_admin()

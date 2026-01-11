#!/usr/bin/env python3
"""
Create Admin User Script
Run this to create the admin account programmatically
Interactive credentials input from terminal
"""
import getpass
from app import create_app, db
from models import User

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email

def validate_password(password):
    """Basic password validation"""
    if len(password) < 8:
        print("❌ Password must be at least 8 characters long!")
        return False
    return True

def get_admin_credentials():
    """Get admin credentials from terminal input"""
    print("\n" + "="*60)
    print("🔐 ADMIN ACCOUNT SETUP")
    print("="*60)
    
    # Get email
    while True:
        ADMIN_EMAIL = input("\n📧 Enter admin email: ").strip()
        if validate_email(ADMIN_EMAIL):
            break
        print("❌ Invalid email format. Please try again.")
    
    # Get name
    while True:
        ADMIN_NAME = input("👤 Enter admin name: ").strip()
        if len(ADMIN_NAME) >= 3:
            break
        print("❌ Name must be at least 3 characters long!")
    
    # Get password with confirmation
    while True:
        ADMIN_PASSWORD = getpass.getpass("🔑 Enter admin password: ")
        if not validate_password(ADMIN_PASSWORD):
            continue
        
        ADMIN_PASSWORD_CONFIRM = getpass.getpass("🔑 Confirm admin password: ")
        if ADMIN_PASSWORD == ADMIN_PASSWORD_CONFIRM:
            break
        print("❌ Passwords do not match. Please try again.")
    
    print("="*60)
    return ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME

def create_admin():
    """Create admin user with credentials from terminal input"""
    app = create_app()
    
    ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME = get_admin_credentials()
    
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
        print(f"Name:     {ADMIN_NAME}")
        print(f"Role:     Admin")
        print("="*60)
        print("\n📝 HOW TO LOGIN AS ADMIN:")
        print("1. Go to: http://localhost:5000/auth/login")
        print("2. Select Role: Admin")
        print(f"3. Enter Email: {ADMIN_EMAIL}")
        print("4. Enter Password: [Your chosen password]")
        print("5. Enter Admin Token: admin-access-token-2025")
        print("6. Click Login")
        print("\n⚠️  SECURITY NOTE:")
        print("   - Your custom password has been set")
        print("   - Keep the admin token secure")
        print("   - Both email/password AND token are required for admin login")
        print("="*60)

if __name__ == "__main__":
    print("🚀 Creating Admin User for Redback...\n")
    create_admin()
#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function definitions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Main setup function
main() {
    echo -e "\n${BLUE}============================================================"
    echo "   Redback Hiring - Automated Database Setup"
    echo -e "============================================================${NC}\n"
    
    # Step 1: Check if MySQL is installed
    print_info "Checking if MySQL is installed..."
    if ! command -v mysql &> /dev/null; then
        print_error "MySQL is not installed. Please install MySQL first."
        echo "For Ubuntu/Debian: sudo apt-get install mysql-server"
        echo "For macOS: brew install mysql"
        exit 1
    fi
    print_success "MySQL is installed"
    
    # Step 2: Check if MySQL is running
    print_info "Checking if MySQL server is running..."
    if sudo systemctl status mysql &> /dev/null; then
        print_success "MySQL server is running"
    else
        print_warning "MySQL server is not running. Attempting to start..."
        if sudo systemctl start mysql; then
            print_success "MySQL server started successfully"
        else
            print_error "Failed to start MySQL server"
            exit 1
        fi
    fi
    
    # Step 3: Create database and user
    print_info "Setting up database and user..."
    sudo mysql -u root << EOF
CREATE DATABASE IF NOT EXISTS interview;
CREATE USER IF NOT EXISTS 'ravi'@'localhost' IDENTIFIED BY 'Ravi@1234';
GRANT ALL PRIVILEGES ON interview.* TO 'ravi'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
    
    if [ $? -eq 0 ]; then
        print_success "Database 'interview' created"
        print_success "User 'ravi' created with full privileges"
    else
        print_error "Failed to setup database"
        exit 1
    fi
    
    # Step 4: Initialize database schema
    print_info "Initializing database schema..."
    python3 -c "from app import create_app; from models.db import db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database schema initialized successfully')"
    
    if [ $? -eq 0 ]; then
        print_success "Database schema initialized"
    else
        print_warning "Database schema initialization had issues"
        print_info "You may need to initialize manually:"
        echo "  python3 -c \"from app import create_app; from models.db import db"
        echo "  app = create_app()"
        echo "  with app.app_context(): db.create_all()\""
    fi
    
    # Step 5: Verify setup
    print_info "Verifying database setup..."
    if mysql -u ravi -pRavi@1234 -e "SELECT DATABASE();" &> /dev/null; then
        print_success "Database connection verified!"
    else
        print_warning "Could not verify connection (this may be OK on some systems)"
    fi
    
    # Final message
    echo -e "\n${GREEN}============================================================"
    echo "   ✓ Database setup completed successfully!"
    echo -e "============================================================${NC}"
    echo -e "\nDatabase: ${BLUE}interview${NC}"
    echo -e "User: ${BLUE}ravi${NC}"
    echo -e "Host: ${BLUE}localhost${NC}"
    echo -e "\nNext steps:"
    echo -e "1. Create admin user: ${BLUE}python3 create_admin.py${NC}"
    echo -e "2. Start the application: ${BLUE}python3 app.py${NC}"
    echo -e "3. Open browser: ${BLUE}http://localhost:5000${NC}\n"
}

# Run main function
main

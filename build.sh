#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Initialize database
python3 << END
from app import app, db
from models import User, HeritageSite, Artisan, Hotel
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@digitalcatalyst.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created')
    else:
        print('Admin user already exists')
    
    print('Database initialized successfully')
END

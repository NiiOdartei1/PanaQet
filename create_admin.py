# create_admin.py

from app import app  # Import your app instance
from database import db  # Import db from database.py
from models import User  # Import your User model

def create_admin_user():
    username = "admin"
    email = "niiodartei24@gmail.com"
    password = "odartei"
    role = "admin"
    country = "DefaultCountry"  # Replace with an appropriate default value

    # Check if the admin user already exists
    with app.app_context():
        existing_admin = User.query.filter_by(email=email).first()
        if existing_admin:
            print("Admin user already exists.")
            return

        # Create the admin user
        new_admin = User(username=username, email=email, role=role, country=country)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully.")

if __name__ == '__main__':
    # Ensure app context is available for the database operations
    with app.app_context():
        create_admin_user()

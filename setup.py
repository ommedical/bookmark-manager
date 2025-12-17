# setup.py
import os
import sys
import secrets
from database import init_db

def setup():
    print("Setting up Bookmark Manager...")
    
    # Generate secret key
    secret_key = secrets.token_hex(32)
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write("FLASK_ENV=development\n")
    
    print(f"✓ Secret key generated: {secret_key[:16]}...")
    
    # Initialize database
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
    
    print("\nSetup complete!")
    print("To run the app: python app.py")
    print("Then open: http://localhost:5000")

if __name__ == "__main__":
    setup()
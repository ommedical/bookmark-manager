import sqlite3
import os
from config import Config

def get_db_connection():
    """Get a database connection (no Flask context needed)"""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Bookmarks table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create indexes for better performance
    conn.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON bookmarks(user_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON bookmarks(created_at DESC)')
    
    conn.commit()
    conn.close()

# For Flask context usage (backward compatibility)
def get_db():
    """Get database connection within Flask context"""
    from flask import g
    if not hasattr(g, 'db'):
        g.db = get_db_connection()
    return g.db

def close_db(e=None):
    """Close database connection"""
    from flask import g
    db = g.pop('db', None)
    if db is not None:
        db.close()
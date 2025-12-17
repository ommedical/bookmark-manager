from flask_login import UserMixin
from database import get_db
from auth import verify_password

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        
        if not user:
            return None
        
        return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])
    
    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if not user:
            return None
        
        return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])
    
    def verify_password(self, password):
        return verify_password(self.password_hash, password)
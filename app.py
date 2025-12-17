from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from database import init_db, get_db, close_db, get_db_connection
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize database before app context
init_db()

# Register close_db to be called when app context ends
app.teardown_appcontext(close_db)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import after app creation to avoid circular imports
from auth import auth_bp
from models import User

@login_manager.user_loader
def load_user(user_id):
    # Use direct connection for login manager
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    
    if not user:
        return None
    
    return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])

# Register authentication blueprint
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    bookmarks = db.execute('''
        SELECT * FROM bookmarks 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (current_user.id,)).fetchall()
    return render_template('dashboard.html', bookmarks=bookmarks)

@app.route('/add_bookmark', methods=['POST'])
@login_required
def add_bookmark():
    title = request.form.get('title')
    url = request.form.get('url')
    tags = request.form.get('tags', '')
    
    if not title or not url:
        flash('Title and URL are required!', 'error')
        return redirect(url_for('dashboard'))
    
    db = get_db()
    db.execute('''
        INSERT INTO bookmarks (user_id, title, url, tags)
        VALUES (?, ?, ?, ?)
    ''', (current_user.id, title, url, tags))
    db.commit()
    
    flash('Bookmark added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_bookmark/<int:bookmark_id>')
@login_required
def delete_bookmark(bookmark_id):
    db = get_db()
    db.execute('DELETE FROM bookmarks WHERE id = ? AND user_id = ?', 
               (bookmark_id, current_user.id))
    db.commit()
    flash('Bookmark deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    db = get_db()
    
    results = db.execute('''
        SELECT * FROM bookmarks 
        WHERE user_id = ? 
        AND (title LIKE ? OR url LIKE ? OR tags LIKE ?)
        ORDER BY created_at DESC
    ''', (current_user.id, f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    
    return render_template('dashboard.html', bookmarks=results, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)
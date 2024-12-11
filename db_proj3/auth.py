# auth.py
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from .db import get_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class User(UserMixin):
    def __init__(self, cid, username, first_name, last_name, role=None):
        self.id = cid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user WHERE cid = %s', (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(
            cid=user_data['cid'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data.get('role')  # 处理角色字段
        )
    return None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('auth/index.html')  # 确保路径正确

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        bill_addr = request.form['billAddr']  # 使用表中定义的字段名
        role = request.form.get('role')  # 获取角色字段，默认为 None

        db = get_db()
        error = None
        cursor = db.cursor()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name or not last_name:
            error = 'Full name is required.'
        else:
            cursor.execute(
                'SELECT 1 FROM user WHERE username = %s', (username,)
            )
            existing_user = cursor.fetchone()
            if existing_user:
                error = f"User {username} is already registered."

        if error is None:
            hashed_password = generate_password_hash(password + current_app.config['SECRET_KEY'])
            try:
                cursor.execute(
                    "INSERT INTO user (first_name, last_name, username, password, billAddr, role) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, username, hashed_password, bill_addr, role),
                )
                db.commit()
            except Exception as e:
                error = str(e)
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )
        user = cursor.fetchone()

        if user is None or not check_password_hash(user['password'], password + current_app.config['SECRET_KEY']):
            flash('Incorrect username or password.')
        else:
            login_user(User(
                user['cid'],
                user['username'],
                user['first_name'],
                user['last_name'],
                user.get('role')  # 加载角色字段
            ))
            return redirect(url_for('auth.index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('base.html')  # 重定向到主页或其他页面
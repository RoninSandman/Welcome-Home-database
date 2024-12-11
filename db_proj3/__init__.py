from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from db_proj3.auth import auth_bp
from db_proj3.items import items_bp
from db_proj3.donations import donations_bp
from db_proj3.config import Config
import os
from flask_login import LoginManager, login_required, current_user
from .orders import orders_bp  # 添加这一行以导入 orders 蓝图
from .items import items_bp

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # 使用绝对导入从 db_proj3.config 中加载配置
    app.config.from_object(Config)

    if test_config is None:
        # 加载实例配置，如果存在的话
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 如果传递了测试配置，则加载它
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化扩展
    login_manager = LoginManager()
    login_manager.init_app(app)

    # 用户加载回调函数
    from db_proj3.models import User  # 假设你有一个 User 模型

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 注册蓝图
    from db_proj3.auth import auth_bp
    from db_proj3.items import items_bp
    from db_proj3.donations import donations_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(donations_bp, url_prefix='/donations')
    app.register_blueprint(orders_bp, url_prefix='/orders')  # 注册 orders 蓝图


    # 添加一个简单的测试路由
    @app.route('/')
    def main_index():
        return render_template('base.html')

    # 初始化数据库命令
    db.init_app(app)

    with app.app_context():
        db.create_all()  # 在应用上下文中创建数据库表格

    return app
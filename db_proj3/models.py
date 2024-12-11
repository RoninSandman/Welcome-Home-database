# models.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db_proj3 import db  # 确保从正确的路径导入 db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    cid = db.Column(db.Integer, primary_key=True)  # 修改为主键 cid
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(50))  # 添加角色字段

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.cid)  # 返回字符串形式的 cid
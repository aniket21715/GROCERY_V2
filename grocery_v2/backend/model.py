from flask_login import UserMixin
from sqlalchemy import create_engine
from app import db ,login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
      
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
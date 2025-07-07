from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(225), nullable=False)
    summaries = db.relationship('Summary', backref='user', lazy=True)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    original_text = db.Column(db.Text)
    summarized_text = db.Column(db.Text)
    created_at = db.Column(db.Integer, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
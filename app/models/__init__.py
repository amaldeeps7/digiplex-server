from flask_sqlalchemy import SQLAlchemy
from app.extensions import db  # Import db from extensions

# db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
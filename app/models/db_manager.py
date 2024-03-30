# app/models/db_manager.py
from . import db, Transaction
from datetime import datetime

class TransactionManager:
    @staticmethod
    def insert_transaction(user_id, amount, purpose):
        print(f"Inserting transaction for user {user_id}")
        transaction = Transaction(user_id=user_id, amount=amount, purpose=purpose)
        db.session.add(transaction)
        db.session.commit()

    def get_transactions_for_month(user_id, year, month):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date
        ).all()
        return transactions

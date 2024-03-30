import psycopg2
from psycopg2 import sql

# A model to manage postgresql. Create table if not available, insert transaction into table, and return success message, if payment is processed.
class TransactionModel:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS transactions (id SERIAL PRIMARY KEY, amount FLOAT, status TEXT)"
        )
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_transaction(self, amount, status):
        insert_query = sql.SQL(
            "INSERT INTO transactions (amount, status) VALUES (%s, %s)"
        )
        self.cursor.execute(insert_query, (amount, status))
        self.conn.commit()

    def process_payment(self, amount):
        # Here you can add your payment processing logic
        # If payment is successful, insert transaction into table
        self.insert_transaction(amount, 'Processed')
        return "Payment is processed successfully"


from flask import request, jsonify
from app.api import bp
from app.models import db, Transaction  # Adjust import to reflect new model usage
from flask_socketio import emit, Namespace
from app.extensions import socketio

@bp.route('/payment', methods=['POST'])
def receive_payment():
    data = request.get_json()
    if not data or 'UserID' not in data or 'Amount' not in data or 'Purpose' not in data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    user_id = data['UserID']
    amount = data['Amount']
    purpose = data['Purpose']

    try:
        transaction = Transaction(user_id=user_id, amount=amount, purpose=purpose)
        db.session.add(transaction)
        db.session.commit()

        # Prepare the payment information to be sent
        payment_info = {
            'UserID': user_id,
            'Amount': amount,
            'Purpose': purpose
        }
        
        # Emit the payment information to connected clients
        update_payment_status(payment_info)  # or notify_payment(payment_info)

    except Exception as e:
        # Log the exception e
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    return jsonify({"status": "success", "message": "Payment processed"}), 200

@bp.route('/latest-transaction', methods=['GET'])
def get_latest_transaction():
    try:
        # Assuming 'Transaction' is your SQLAlchemy model and it has an 'id' field
        # If you have a timestamp field, you can order by that field instead
        latest_transaction = Transaction.query.order_by(Transaction.id.desc()).first()
        
        if latest_transaction:
            # Prepare and return the transaction data as JSON
            transaction_data = {
                'UserID': latest_transaction.user_id,
                'Amount': latest_transaction.amount,
                'Purpose': latest_transaction.purpose,
                # Include other fields as necessary
            }
            return jsonify(transaction_data), 200
        else:
            return jsonify({"message": "No transactions found"}), 404
    except Exception as e:
        # Log the exception
        print(e)
        return jsonify({"status": "error", "message": "Internal server error"}), 500


# Function to be called when a payment is processed
# def notify_payment(payment_info):
#     # Emit a 'payment_received' event to connected clients
#     emit('payment_received', payment_info, broadcast=True)

class PaymentStatusNamespace(Namespace):
    def on_connect(self):
        print('Client connected')

    def on_disconnect(self):
        print('Client disconnected')

    # You can add more event handlers here as needed

# Register the namespace
socketio.on_namespace(PaymentStatusNamespace('/paymentstatus'))


# Function to call when updating payment status
def update_payment_status(payment_info):
    # Emit a 'payment_update' event to all clients connected to /paymentstatus
    socketio.emit('payment_update', payment_info, namespace='/paymentstatus')
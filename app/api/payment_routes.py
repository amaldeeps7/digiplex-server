from flask import request, jsonify
from app.api import bp
from app.models import db, Transaction  # Adjust import to reflect new model usage

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
    except Exception as e:
        # Log the exception e
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    return jsonify({"status": "success", "message": "Payment processed"}), 200

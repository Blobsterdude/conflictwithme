from paypalrestsdk import Payment, configure
from flask import Flask, request, jsonify, url_for,render_template,redirect,flash
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from paymentService import Payments
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Configure PayPal SDK
mode = os.environ.get('PAYPAL_MODE')
client_id = os.environ.get('PAYPAL_CLIENT_ID')
client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')


configure({
    "mode": mode,
    "client_id": client_id,
    "client_secret": client_secret
})

# Create Flask app
app = Flask(__name__)
CORS(app)

# create database engine
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/payment')
Payments.metadata.create_all(engine)
# create a session factory
Session = sessionmaker(bind=engine)

# Create a route to generate a PayPal payment URL
@app.route('/create-payment', methods=['POST'])
def create_payment():
    payment_data = request.get_json()
    amount = payment_data['amount']
    invoice_no = payment_data['invoiceNo']
    # return jsonify(payment_data)
    print(payment_data) 
    # amount = request.form.get('amount')

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('execute_payment', invoice_no=invoice_no, _external=True),
            "cancel_url": url_for('cancel_payment', _external=True)
        },
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "SGD"
            },
            "description": "Whale Clinic Payment"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return jsonify({'url': link.href})
    else:
        return jsonify({'error': payment.error})

# Create a route to execute the PayPal payment
@app.route('/execute-payment', methods=['GET'])
    
# def execute_payment():
#     payment_id = request.args.get('paymentId')
#     payer_id = request.args.get('PayerID')
#     invoice_no = request.args.get('invoice_no')
#     print(payment_id, payer_id,invoice_no)

#     payment = Payment.find(payment_id)

#     if payment.execute({"payer_id": payer_id}):

#         success_msg = "Payment successful."
        
#         # create a new session
#         session = Session(bind=engine)

#         # update the payment status in the database
#         payment = session.query(Payments).filter_by(invoiceNo=invoice_no).first()
#         payment.paymentStatus = 'Paid'
#         session.commit()

#         return success_msg
#     else:
#         return "Payment failed."

def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    invoice_no = request.args.get('invoice_no')
    print(payment_id, payer_id,invoice_no)
    payment = Payment.find(payment_id)

    try:
        # execute the payment and check the result
        result = payment.execute({"payer_id": payer_id})

        if result:
            success_msg = "Payment successful."
            
            # create a new session
            session = Session(bind=engine)

            # update the payment status in the database
            payment = session.query(Payments).filter_by(invoiceNo=invoice_no).first()
            payment.paymentStatus = 'Paid'
            session.commit()
            
            return "Successful Payment"
        else:
            return "Payment failed."

    except Exception as e:
        # handle the exception
        return "Payment failed. Reason: " + str(e)
    
# Create a route to cancel the PayPal payment
@app.route('/cancel-payment', methods=['GET'])
def cancel_payment():
    return "Payment canceled."

# Run the app
if __name__ == '__main__':
    app.run(port=5300 ,debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/payment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)



class Payments(db.Model):
    __tablename__ = 'payment'


    invoiceNo = db.Column(db.String, primary_key=True)
    paymentStatus = db.Column(db.String(50), nullable=False)
    patientID = db.Column(db.Integer, nullable=False)
    payDate = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)


    def __init__(self, invoiceNo, paymentStatus, patientID, payDate, amount):
        self.invoiceNo = invoiceNo
        self.paymentStatus = paymentStatus
        self.patientID = patientID
        self.payDate = payDate
        self.amount = amount


    def json(self):
        return {"invoiceNo": self.invoiceNo, "paymentStatus": self.paymentStatus, "patientID": self.patientID, "payDate": self.payDate, "amount": self.amount}



@app.route("/payment")
def get_all():
    paymentlist = Payments.query.all()
    if len(paymentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payment": [payment.json() for payment in paymentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404

@app.route("/payment/<string:parameter>")
def get_all_filter(parameter):
    parameter = parameter[-4:]
    paymentlist = Payments.query.filter_by(patientID=parameter).all()
    if len(paymentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payment": [payment.json() for payment in paymentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404


@app.route("/payment/<string:invoiceNo>")
def find_by_invoiceNo(invoiceNo):
    payment = Payments.query.filter_by(invoiceNo=invoiceNo).first()
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Payment not found."
        }
    ), 404

@app.route("/payment/amount/<string:invoiceNo>")
def find_invoiceNo_amount(invoiceNo):
    payment = Payments.query.filter_by(invoiceNo=invoiceNo).first()
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()['amount']
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Payment not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5600, debug=True)
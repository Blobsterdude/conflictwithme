from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from os import environ
from flask_cors import CORS

import amqp_setup
import json
import os

app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/ESD_project'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/medicine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Medicine(db.Model):
    __tablename__ = 'medicine_inventory'

    # medicineID = db.Column(db.Integer(), primary_key=True)
    medicineName = db.Column(db.String(1000), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    lowStock = db.Column(db.Integer, nullable=False)

    def __init__(self, medicineName, quantity, lowStock):
        # self.medicineID = medicineID
        self.medicineName = medicineName
        self.quantity = quantity
        self.lowStock = lowStock

    def json(self):
        return {
                "medicineName": self.medicineName, 
                "quantity": self.quantity,
                "lowStock": self.lowStock}

# to send alerts to admin ui for low stock meds
@app.route('/medicine/admin', methods=['GET', 'POST'])
def get_low_stock_medicine():
    low_stock_med = []
    medicines = Medicine.query.filter(Medicine.quantity<10)
    for medicine in medicines:
        medicine_dict = {
            'medicineName': medicine.medicineName,
            'quantity': medicine.quantity
        }
        low_stock_med.append(medicine_dict)
    return jsonify(low_stock_med)

@app.route("/medicine" , methods=['GET','POST'])
def get_all():
    inventory = Medicine.query.all()
    if len(inventory):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [medicine.json() for medicine in inventory]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Whale Clinic has completely run out of medicine."
        }
    ), 404

@app.route("/medicine/<string:medicineName>" , methods=['PUT'])
def update_inventory(medicineName):
    # return medData
    # Update the inventory in the database
    medData = request.json
    # return medData
    medicineName = medData['medName']
    quantity = medData['quantity']
    try:
        medicine = Medicine.query.filter_by(medicineName=medicineName).first()
        # return order
        if not medicine:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "medicineName": medicineName
                    },
                    "message": "Medicine not found."
                }
            ), 404
        # update status
        # return medData
        # return jsonify (
        #     quantity
        # )
        else:
            medicine.quantity = quantity
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": medicine.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "medicineName": medicineName
                },
                "message": "An error occurred while updating the medicine quantity. " + str(e)
            }
        ), 500


@app.route("/medicine/update>", methods=['POST','PUT','GET'])
def create_medicine(medicineName):
    if (Medicine.query.filter_by(medicineName=medicineName).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "medicineName": medicineName
                },
                "message": "Medicine already exists."
            }
        ), 400


    data = request.get_json()
    new_medicine = Medicine(medicineName, **data)


    try:
        db.session.add(new_medicine)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "medicineName": medicineName
                },
                "message": "An error occurred creating the medicine."
            }
        ), 500

    return jsonify(
        
        {
            "code": 201,
            "data": new_medicine.json()
        }
    ), 201

monitorBindingKey = '#'

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    print(json.loads(body))
    processMedicineLog(json.loads(body))
    print() # print a new line feed

def receiveMedicineLog():
    amqp_setup.check_setup()
    queue_name = 'medicine'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 

    
    
    print('i am inside the function')
    
    
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


 

# def processMedicineLog(medicine):
#     print("Recording an order log:")
#     print('hi')
#     print(medicine)
#     print('bye')
#     with app.app_context():
#         medicineName = medicine["medicineName"]
#         quantity = medicine["medicineQty"]
#         lowStock = 1
#         # medicineID = 88887777
    
#         medicine = Medicine(lowStock=lowStock, quantity=quantity,medicineName=medicineName)
     
#         try:
#             print('bro')
#             db.session.add(medicine)
#             db.session.commit()
        
#             print("Queue item enqueued successfully")
#         except:
#             print("An error occurred while enqueuing the message")
def processMedicineLog(medicine):
    print("Recording an order log:")
    print(medicine)

    with app.app_context():
        medicineName = medicine["medicineName"]
        is_medicine = Medicine.query.filter_by(medicineName=medicineName).first()

        if not is_medicine:
            print(f"Medicine {medicineName} not found.")
            return

        if is_medicine.quantity < 1:
            print(f"No stock available for {medicineName}.")
            return

        is_medicine.quantity -= int(medicine["medicineQty"])

        try:
            db.session.commit()
            print("Medicine quantity updated successfully.")
        except:
            db.session.rollback()
            print("An error occurred while updating the medicine quantity.")



if __name__ == '__main__':
    app.run(port=8000, debug=True, use_reloader=False)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveMedicineLog()
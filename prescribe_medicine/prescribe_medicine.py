from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
import amqp_setup
import pika
import json
import logging
app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)

queue_URL = 'http://127.0.0.1:5004/queue'
medicine_URL = 'http://127.0.0.1:8000/medicine'

@app.route("/prescribe_medicine", methods=['POST'])
def prescribe_medicine():
    # Simple check of input format and data of the request are JSON


    data = request.get_json()
    # {'patientId': '3', 'medicineName': '1', 'medicineQty': 1}
    # patientID= {"patientId": data['patientId']}
    # print(patientID)
    # {'patientId': '3'}
    medicineName = {"medicineName": data['medicineName']}
    medicineQty = {"medicineQty": data['medicineQty']}

    # return jsonify(patientID)
    # Publish the patientId message with routing_key = patientId
    print('\n\n-----Publishing the patientId message with routing_key patientId-----')

    message = json.dumps(data)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\npatient id published to RabbitMQ Exchange.\n")
    # 7. Return success
    return {
        "code": 200,

        "data": {"result": message},
        "message": "success"
    }, 200
    
if __name__ == "__main__":
    app.run( port=5200, debug=True)
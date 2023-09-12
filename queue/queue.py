from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from invokes import invoke_http

import amqp_setup
import json
import os

monitorBindingKey='#'

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/queue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

queue_URL = "http://localhost:5004/queue"

db = SQLAlchemy(app)
class Queue(db.Model):
    __tablename__ = 'queue'
    # queueId = db.Column(db.Integer, nullable=False, primary_key=True)
    patientId = db.Column(db.String, nullable=False, primary_key=True)
    medicineNeeded = db.Column(db.JSON, nullable=False)
    is_served = db.Column(db.Integer, nullable=False)

    def __init__(self, patientId, medicineNeeded, is_served):
        # self.queueId = queueId
        self.patientId = patientId
        self.medicineNeeded = medicineNeeded
        self.is_served = is_served

    def json(self):
        return {
                "patientId": self.patientId,
                "medicineNeeded": self.medicineNeeded, "is_served": self.is_served
            }


@app.route("/queue", methods=['POST'])
def create_queue(data):
    # data = request.json
    print (jsonify(data))
    patientId = data['patientId']
    medicineName = data['medicineName']
    quantity = data['medicineQty']
    medicineNeeded = {"medicine": [{"name": medicineName, "quantity": quantity}]}
    # queueId = data['queueId']
    # medicineNeeded = jsonify(medicineNeeded)
    is_served = 0
    queue = Queue(patientId=patientId, medicineNeeded=medicineNeeded,  is_served=is_served)
    try:
        db.session.add(queue)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": queue.json(),
                "message": "Queue item enqueued successfully"
            }
        ), 201
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "patientId": patientId,
                     "medicineNeeded": medicineNeeded,
                    "is_served": is_served,
                },
                "message": "An error occurred while enqueuing the message"
            }
        ), 500

@app.route("/queue", methods=['DELETE'])
def dequeue_message():
    # Find the first item in the queue (i.e. the one with the smallest queueId)
    queue_item = Queue.query.order_by(Queue.patientId).first()
    if not queue_item:
        return jsonify(
            {
                "code": 404,
                "message": "Queue is empty"
            }
        ), 404

    # Remove the item from the database
    db.session.delete(queue_item)
    db.session.commit()

    return jsonify(
        {
            "code": 200,
            "data": queue_item.json(),
            "message": "Queue item dequeued successfully"
        }
    ), 200


@app.route('/queue', methods=['GET'])
def get_queue():
    queueList = Queue.query.all()
    if len(queueList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "queues": [queue.json() for queue in queueList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no queues."
        }
    ), 404

# lab 6, 

@app.route('/queue/<patientId>', methods=['GET'])
def get_queue_item(patientId):
    queue_item = Queue.query.filter_by(patientId=patientId).first()
    if queue_item is not None:
        return jsonify(queue_item.json())
    else:
        return jsonify({'message': 'Queue item not found'})
    

monitorBindingKey='#'

def receiveQueueLog():
    amqp_setup.check_setup()
    # print ("hi receive queue log")
    queue_name = 'queue'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    # print ('alan megagrle')

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    print(json.loads(body))
    
    processQueueLog(json.loads(body))
    # json.loads(body) will get the json data
    # and then you should create funciton to add it into the database
    
    print() # print a new line feed
    
    # when queue microservice receive 
    # write adding to the queue microservice


def processQueueLog(queue):
    print("Recording an order log:")
    # print('hi')
    print(queue)
    with app.app_context():
        patientId = queue["patientId"]
        medicineName = queue["medicineName"]
        quantity = queue["medicineQty"]
        medicineNeeded = {"medicine": [{"name": medicineName, "quantity": quantity}]}
        is_served = 0
        print(json.dumps(medicineNeeded))
        medicineNeeded = json.dumps(medicineNeeded)
        # medicineNeeded = jsonify({"medicine": [{"name": medicineName, "quantity": jsonify(quantity)}]})

        queue = Queue(patientId=patientId, medicineNeeded=medicineNeeded, is_served=is_served)
        # {
        #   "medicine": [
        #     {
        #       "name": "Medicine E",
        #       "quantity": 2
        #     }
        #     ,
        #     {
        #       "name": "Medicine F",
        #       "quantity": 1
        #     }
        #   ]
        # }
        
        try:
            print(queue)

            db.session.add(queue)
            db.session.commit()
        # print('bro')
            print("Queue item enqueued successfully")
        except:
            print("An error occurred while enqueuing the message")

if __name__ == '__main__':
    app.run(port=5004, debug=True,use_reloader=False)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveQueueLog()
    
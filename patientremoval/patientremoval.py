from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/queue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
class Queue(db.Model):
    __tablename__ = 'queue'

    queueId = db.Column(db.Integer, nullable=False, primary_key=True)
    patientId = db.Column(db.Integer, nullable=False)
    medicineNeeded = db.Column(db.JSON, nullable=True)
    is_served = db.Column(db.Integer, nullable=False)

    def __init__(self, queueId, patientId, medicineNeeded, is_served):
        self.queueId = queueId
        self.patientId = patientId
        self.medicineNeeded = medicineNeeded
        self.is_served = is_served

    def json(self):
        return {
            "queueId": self.queueId, "patientId": self.patientId,
            "medicineNeeded": self.medicineNeeded, "is_served": self.is_served
        }
 
# This microservice will listen for POST requests to /collectMedicine. 
# It will then send a GET request to the queue service to get the next patient in the queue,
#  and a GET request to the medicine service to get details about the medicine that the patient needs. 
# It will then send a DELETE request to the queue service to remove the patient from the queue. 
# Finally, it will return a response with the patient ID and medicine details.
#  If there are no patients in the queue, it will return a 404 error.
@app.route("/patientremoval", methods=['GET','POST','PUT'])
def collectMedicine():

    # Get next patient in queue information
    queue_url = f"http://localhost:5004/queue"
    queue_response = requests.get(queue_url)
    queue_data = queue_response.json().get("data")
    
    if queue_data:
          # Send request to remove patient from queue
        queue_item_url = f"http://localhost:5004/queue"
        queue_item_response = requests.delete(queue_item_url)

        if queue_item_response.status_code != 204:
            return jsonify(
                {
                    "code": 200,
                    "message": "Removed a patient from queue"
                }
            ), 200


    else:
        return jsonify(
            {
                "code": 404,
                "message": "There are no patients in queue"
            }
        ), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)




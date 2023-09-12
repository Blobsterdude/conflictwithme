from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.dialects.postgresql import JSONB
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Patient(db.Model):
    __tablename__ = 'patient'

    patientID = db.Column(db.String(64), nullable=False, primary_key=True)
    patientName = db.Column(db.String(64), nullable=False)
    dob = db.Column(db.String(64), nullable=False)
    nric = db.Column(db.String(64), nullable=False)
    addr = db.Column(db.String(64), nullable=False)
    mobileno = db.Column(db.String(64), nullable=False)


    def __init__(self, patientID, patientName, dob, nric, addr, mobileno):
        self.patientID = patientID
        self.patientName = patientName
        self.dob = dob
        self.nric = nric
        self.addr = addr
        self.mobileno = mobileno
    
    def json(self):
        return {"patientID": self.patientID, "patientName": self.patientName, 
                "dob": self.dob, "nric": self.nric, "mobileno": self.mobileno, 
                "addr": self.addr
               }

@app.route("/patient")
def get_all():
    all_patient = Patient.query.all()
    if len(all_patient):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "patient": [row.json() for row in all_patient]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no patients."
        }
    ), 404
    
@app.route("/patient/<string:patient_id>")
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    print(patient)
    if patient:
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Patient not found"
        }
    ), 404
    
@app.route("/patient/create", methods=["POST"])
def create_patient():
    data = request.get_json()
    # return data
    patientData = data['patientData']
    # return patientData
    patientName = patientData['name']
    dob = patientData['dob']
    nric = patientData['uinfin']
    addr = patientData['regadd']
    patientID = nric[5:]
    mobileno = patientData['mobileno']
   
    # patientID = jsonify(patientID)
    # return patientID
    # return jsonify(mobile)
    # patient = Patient.query.filter_by(patientId=patientId).first()
    if (Patient.query.filter_by(patientID=patientID).first()):
        return jsonify(
            {
            "code": 400,
                "data": {
                    "patientID": patientID
                },
                "message": "Patient record exists."
            }
        ), 400
    patient = Patient(patientID, patientName, dob, nric, addr, mobileno)

    try:
        db.session.add(patient)
        # return jsonify ("Hello")
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "patientID": patientID
                },
                "message": "An error occurred creating the patient record"
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": patient.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)
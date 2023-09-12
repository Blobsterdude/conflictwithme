from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
import ast
import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/appointment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class NewAppt(db.Model):
    __tablename__ = 'appointment'

    appointmentID = db.Column(db.Integer, primary_key=True)
    # doctorID = db.Column(db.Integer, nullable=False)
    doctorID = db.Column(db.Integer, nullable=False, index=True)
    patientID = db.Column(db.String(64), nullable=False)
    patientName = db.Column(db.String(64), nullable=False)
    # date = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64), nullable=False, index=True)
    # time = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False, index=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    # doctor = db.relationship('Schedule', primaryjoin='NewAppt.doctorID == Schedule.doctorID', backref='doctor_appointments')
    # date_r = db.relationship('Schedule', primaryjoin='NewAppt.date == Schedule.date', backref='date_appointments')
    # time_r = db.relationship('Schedule', primaryjoin='NewAppt.time == Schedule.time', backref='time_appointments')

    def __init__(self, appointmentID, doctorID, patientID, patientName, date, time, created):
        self.appointmentID = appointmentID
        self.doctorID = doctorID
        self.patientID = patientID
        self.patientName = patientName
        self.date = date
        self.time = time 
        self.created = created

    def json(self):
        return {"appointmentID": self.appointmentID, 
                "doctorID": self.doctorID, 
                "patientID": self.patientID, 
                "patientName": self.patientName, 
                "date": self.date, "time": self.time, 
                "created": self.created
                }
        
@app.route("/appointment")
def get_all():
    all_appointment = NewAppt.query.all()
    if len(all_appointment):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "appointment": [row.json() for row in all_appointment]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no available appointments."
        }
    ), 404

@app.route("/appointment/appointmentID")
def find_by_appt_id(appointmentID):
    appt = NewAppt.query.filter_by(appointmentID=appointmentID).first()
    if appt:
        return jsonify(
            {
                "code": 200,
                "data": appt.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "appointmentID": appointmentID
            },
            "message": "Appointment not found."
        }
    ), 404

@app.route("/appointment/create", methods=['POST'])
def create_appointment():
    data = request.get_json()
    # print(data)
    latest_appointment = NewAppt.query.order_by(NewAppt.appointmentID.desc()).first()

    if latest_appointment:
        appointmentID = latest_appointment.appointmentID + 1
        # print(appointmentID)
    else:
        appointmentID = 1
        
    appointmentData = data['appointment']
    patientData = data['patientData']
    patientName = patientData['name']
    print(patientName)
    nric = patientData['uinfin']
    patientID = nric[5:]
    
    # return appointmentData
    date = appointmentData['date']
    doctorName = appointmentData['doctorName']
    doctorID = appointmentData['doctorID']
    time = appointmentData['time']
    created = datetime.datetime.now()
    appointment = NewAppt(appointmentID=appointmentID, doctorID=doctorID, patientID=patientID, patientName=patientName, 
                          date=date, time=time, created=created)
    db.session.add(appointment)
    db.session.commit()
    return jsonify(
        {
            "code": 201,
            "data": {
                "appointment": appointment.json(), 
            }
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5700, debug=True)


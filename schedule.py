from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Schedule(db.Model):
    __tablename__ = 'schedule'

    doctorID = db.Column(db.Integer, nullable=False, primary_key=True)
    doctorName = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64), primary_key=True, nullable=False)
    time = db.Column(db.Integer, primary_key=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False)

    def __init__(self, doctorID, doctorName, date, time, available):
        self.doctorID = doctorID
        self.doctorName = doctorName
        self.date = date
        self.time = time 
        self.available = available

    def json(self):
        # dto = {
        #     "doctorID": self.doctorID, "doctorName": self.doctorName, "date": self.date, "time": self.time, "available": self.available
        # }
        return {
                "doctorID": self.doctorID, "doctorName": self.doctorName, "date": self.date, "time": self.time, "available": self.available
            }

@app.route("/schedule",methods = ['GET'])
def get_all():
    all_schedule = Schedule.query.all()
    print(all_schedule)
    if len(all_schedule):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "schedule": [row.json() for row in all_schedule]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no available appointment slots."
        }
    ), 404

@app.route("/schedule/<int:doctorID>", methods=['GET'])
def find_by_docID(doctorID):
    doctor = Schedule.query.filter_by(doctorID=doctorID).all()
    if doctor:

        output = [x.json() for x in doctor]
        print (output)
        return jsonify(
            {
                "code": 200,
                "data": output
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Doctor not found."
        }
    ), 404

# find by doctor and date 
@app.route("/schedule/<doctorID>/<date>", methods=['GET'])
def find_by_docID_and_date(doctorID, date):
    
    available = Schedule.query.filter_by(doctorID=doctorID, date=date).all()

    if available:
        print(available)
        # output = []
        # for schd in available:
        #     schj = schd.json()
        #     output.append(schj)
        output = [x.json() for x in available]
        print (output)
        return jsonify(
            {
              "code": 200,
              "data": output 
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Appointment date not available."
        }
    ), 404
    
@app.route("/schedule/update",methods = ['PUT'])
def changeSchedule():
    rawData = request.get_json()
    data = rawData['appointment']
    doctorID = data['doctorID']
    date = data['date']
    time = data['time']
    del_appointment = Schedule.query.filter_by(doctorID=doctorID,date=date,time=time).first()
    
    if  del_appointment:
        del_appointment.available = False
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "doctorID": doctorID,
                    "date": date,
                    "time": time

                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                 "doctorID": doctorID,
                 "date": date,
                 "time": time
            },
            "message": "Schedule not updated."
        }
    ), 404
    

if __name__ == '__main__':
    app.run(port=5701, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

# import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

schedule_URL = "http://127.0.0.1:5701/schedule"
appointment_URL = "http://127.0.0.1:5700/appointment" 
patient_URL = "http://127.0.0.1:5001/patient" 


@app.route("/book_appt", methods=['POST'])
def book_appt():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        # return (request.get_json())
        try:
            data = request.get_json()
            # return data
            print("\nAppt booked in JSON:", data)

            # do the actual work
            # 1. Send appt info 
            result = processBookAppt(data)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "book_appt.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processBookAppt(data):
    # 2. Send the appt info
    # Invoke the appt microservice
    # return data
    print('\n-----Invoking appt microservice-----')
    appt_result = invoke_http(appointment_URL + "/create", method='POST', json=data)
    print('appt_result:', appt_result)
  
    # Check the appt result; if a failure, send it to the error microservice.
    code = appt_result["code"]
    message = json.dumps(appt_result)

    # amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as appt fails-----')
        print('\n\n-----Publishing the (appt error) message with routing_key=appt.error-----')
        return {
            "code": 500,
            "data": {"appt_result": appt_result},
            "message": "Appt creation failure sent for error handling."
        }
    
    return {
        "code":201,
        "data":{
            
        },
        "Message":"Appointment Record Created"
    }

@app.route("/updateSchedule", methods=['POST'])
def updateSchedule():
    if request.is_json:
        # return (request.get_json())
        print(request.get_json)
        try:
            data = request.get_json()
            # return data
            print("\nAppt booked in JSON:", data)

            result = updateSch(data)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "book_appt.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def updateSch(result):
    print('\n-----Invoking schedule microservice-----')
    sch_result = invoke_http(schedule_URL + "/update", method='PUT', json=result)
    print('sch_result:', sch_result)
  
    # Check the appt result; if a failure, send it to the error microservice.
    code = sch_result["code"]
    message = json.dumps(sch_result)

    # amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as appt fails-----')
        print('\n\n-----Publishing the (schedule error) message with routing_key=schedule.error-----')
        return {
            "code": 500,
            "data": {"sch_result": sch_result},
            "message": "Schedule update failure sent for error handling."
        }
    
    return {
        "code":201,
        "data":{
            
        },
        "Message":"Appointment Record Created"
    }

@app.route("/addPatient", methods=['POST'])
def addPatient():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        # return (request.get_json())
        try:
            data = request.get_json()
            # return data
            print("\nAppt booked in JSON:", data)

            # do the actual work
            # 1. Send appt info 
            result = updatePatient(data)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "book_appt.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def updatePatient(data):
    # 2. Send the patient info
    # Invoke the Patient microservice
    # return data
    print('\n-----Invoking patient microservice-----')
    patient_result = invoke_http(patient_URL + "/create", method='POST', json=data)
    print('patient_result:', patient_result)
  
    # Check the appt result; if a failure, send it to the error microservice.
    code = patient_result["code"]
    message = json.dumps(patient_result)

    # amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as appt fails-----')
        print('\n\n-----Publishing the (patient error) message with routing_key=patient.error-----')
        return {
            "code": 500,
            "data": {"patient_result": patient_result},
            "message": "Patient record creation failure sent for error handling."
        }
    
    return {
        "code":201,
        "data":{
            
        },
        "Message":"Patient Record Created"
    }
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for booking an appointment, updating schedule and adding patient...")
    app.run(port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.

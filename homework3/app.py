
from flask import Flask, jsonify, render_template, request

import pymongo
from datetime import datetime


numOfApplication = 0

client = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = client["scsu_loans"]
applications = mydb["applications"]

app = Flask(__name__)

     
#adds in a new application
@app.route('/api/add_app', methods=['POST'])
def add_app():
    
    print("Adding an application")
    data = request.get_json()
    application_id = applications.count_documents({})
    
    newApplication = {
        "application_id": application_id,
        "name": data.get("name"),
        "address": data.get("addressOfPerson"),
        "zipcode": data.get("zip"),
        "creditScore": data.get("credit_score"),
        "income": data.get("annualIncome"),
        "status": "received",
        "notes": []
    }
    
   #Inserts application document to database
    applications.insert_one(newApplication)
    
    return jsonify({'message': 'Application added successfully', "application_id": application_id}), 200




#Process an application
@app.route('/api/processApplication/<appToProcess>', methods=['GET'])
def processApplication(appToProcess):
    print(f"Processing application {appToProcess}")
    appNumToProcess = applications.find_one({"application_id": int(appToProcess)})

    #Checks if the application exists
    if appNumToProcess:
        income = int(appNumToProcess.get("income"))
        creditScore = int(appNumToProcess.get("creditScore"))

        #Subphases- Credit check and income check
        creditMessage = ''
        incomeMessage = ''

        #subphase 1- credit check
        if creditScore >= 800:
            #Subphase 2- Income Check
            creditMessage = "Excellent Credit"
            if income >= 60000:
                subphase = "Income Check"
                status = "Accepted"
                incomeMessage = "Accept this person with 5% interest rate."
            else:
                subphase = "Income Check"
                status = "Accepted"
                incomeMessage = "Accept this person with 8% interest rate."
            
        elif creditScore >= 740:
            creditMessage = "Good Credit"
            #Subphase 2- Income Check
            if income >= 70000:
                subphase = "Income Check"
                status = "Accepted"
                incomeMessage = "Accept this person with 12% interest rate."
            else:
                subphase = "Income Check"
                status = "Rejected"
                incomeMessage = "Reject this person for not enough income given the credit score"
            
        elif creditScore >= 670:
            creditMessage = "Fair Credit"
            #Subphase 2- Income Check
            if income >= 80000:
                subphase = "Income Check"
                status = "Accepted"
                incomeMessage = "Accept this person with 15% interest rate."
            else:
                subphase = "Income Check"
                status = "Rejected"
                incomeMessage = "Reject this person for not enough income given the credit score"
        elif creditScore >= 580:
            creditMessage = "Poor Credit"
            #Subphase 2- Income Check
            if income >= 100000:
                subphase = "Income Check"
                status = "Accepted"
                incomeMessage = "Accept this person with 25% interest rate."
            else:
                subphase = "Income Check"
                status = "Rejected"
                incomeMessage = "Reject this person for not enough income given the credit score"
        else:
            subphase = "Credit Check"
            status = "Rejected"
            creditMessage = "Very Bad Credit"
            incomeMessage = "Reject this person for too low"

        
    
    else:
        return jsonify({'message': "Application does not exist"}), 400
    
    updateNote={"$push":{
        "notes":{
            "subphase": subphase,
            "note": creditMessage + ": " + incomeMessage
        }
    }
    }
    updateStatus = {"$set": {"status": status}}
    updateOperation = {**updateStatus, **updateNote}
    applications.update_one(appNumToProcess, updateOperation)
    
    return jsonify({'creditMessage': creditMessage, 'incomeMessage': incomeMessage}), 200



    

#Checks the status of an application
@app.route('/api/check_status/<app_id>', methods=['GET'])
def check_status(app_id):
    print(f"Looking for application with ID: {app_id}")

    applicationToDisplay = applications.find_one({"application_id": int(app_id)})

    if applicationToDisplay:
        return jsonify({"status": applicationToDisplay.get("status", "Unknown"),
                        "notes": applicationToDisplay.get("notes", [])})
    else:
        return jsonify({"message": "Application not found"}), 404



#Api to update the status of the application
@app.route('/api/update_status', methods=['POST']) 
def update_status():
    print("Updating status")

    jsonData = request.get_json()
    app_id = int(jsonData.get("application_id"))
    new_status = jsonData.get("new_status")
    newSubphase = jsonData.get("subphase")
    note = jsonData.get("note", "").strip()

    data = {"newStatus": {'notFound', 'received', 'processing', 'accepted', 'rejected'}}
    data["newStatus"] = list(data["newStatus"])

    applicationToUpdate = applications.find_one({"application_id": int(app_id)})

    if applicationToUpdate:
        updateApp = {"application_id": app_id}
        updateStatus = {"$set": {"status": new_status}}
        
        if note: 
       
            updateNote = {"$push": {
                "notes": {
                    "subphase": newSubphase,
                    "note": note
                }
            } }
                
                

            updateOperation = {**updateStatus, **updateNote}
        else:
            updateOperation = updateStatus
        
        applications.update_one(updateApp, updateOperation)
        

        return jsonify({"message": f"Application {app_id} status updated to '{new_status}'"}), 200
    

    else:
        return jsonify({"message": "Application not found"}), 404

    

#returns the render template
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)

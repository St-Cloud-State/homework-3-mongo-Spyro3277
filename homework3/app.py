
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
        "status": "received",
        "notes": []
    }
    
   #Inserts application document to database
    applications.insert_one(newApplication)
    
    return jsonify({'message': 'Application added successfully', "application_id": application_id}), 200

#Checks the status of an application
@app.route('/api/check_status/<app_id>', methods=['GET'])
def check_status(app_id):
    print(f"Looking for application with ID: {app_id}")

    applicationToDisplay = applications.find_one({"application_id": int(app_id)})

    if applicationToDisplay:
        return jsonify({"status":applicationToDisplay["status"]})
    else:
        return jsonify({"message": "Application not found"}), 404



#Api to update the status of the application
@app.route('/api/update_status', methods=['POST']) 
def update_status():
    print("Updating status")

    jsonData = request.get_json()
    app_id = int(jsonData.get("application_id"))
    new_status = jsonData.get("new_status")
    note = jsonData.get("note", "").strip()

    data = {"newStatus": {'notFound', 'received', 'processing', 'accepted', 'rejected'}}
    data["newStatus"] = list(data["newStatus"])

    applicationToUpdate = applications.find_one({"application_id": int(app_id)})

    if applicationToUpdate:
        updateApp = {"application_id": app_id}
        updateStatus = {"$set": {"status": new_status}}
        
        if note: 
       
            updateNote = {"$push": {"notes": note}}

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

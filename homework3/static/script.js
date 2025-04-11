const applications = []

//Adds an application into a list
function addApp(){
    const appName = document.getElementById('appName').value;
    const zipCode = document.getElementById('zipCode').value;
    const address = document.getElementById('address').value;
   

    const appData ={
        name: appName,
        zip: zipCode,
        addressOfPerson: address,
            
    };

    fetch('/api/add_app',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(appData)
    })
        .then(response => response.json())
        .then(data =>{
            console.log("Data received:", data);
            const appID = data.application_id;

            applications.push({...appData, application_id: appID});
            

            
            alert(`Application submitted. ID: ${appID}`)

        })

        .catch(error =>{
            console.error('Error adding application', error);
            alert("Something went wrong :(")
        });
        


}

//Shows an application
function displayAnApplication(){
    const appList = document.getElementById('appList');
    appList.innerHTML = '';

    applications.forEach(app => { 
        const appElement = document.createElement('div');
        appElement.innerHTML = `
        <p>Application Name: ${app.name}<br>
        Zipcode: ${app.zip}<br>
        Application Number: ${app.serialNumber}<br>
        Address: ${app.addressOfPerson} <br>
        Status: ${app.status} </p>
        `;
        appList.appendChild(appElement);

    });

}



//Displays the status of an application
function displayStatus(){
    const numToCheck = document.getElementById('checkStatus').value;
  
    fetch(`/api/check_status/${numToCheck}`)
        .then(response =>{
            if (!response.ok) {
                throw new Error("Application not found");
            }
            return response.json();
        })

        .then(data =>{
            console.log(data);

            const showStatus = document.getElementById('showStatus');
            showStatus.innerHTML = `
            <p>
            Application number ${numToCheck} status: ${data.status} <br>
            Notes: <br>
            ${data.note}
            
            </p>
            
            `;
            
        })
        .catch(error => {
            console.error(error);
            document.getElementById('showStatus').innerHTML = "<p>Application not found.</p>";
        });
   

}

//Api to updating the status
function updateStatus(){

    const appToChange = document.getElementById('appNumToUpdate').value;
    const newStatusValue = document.getElementById('newStatus').value;
    const newNote = document.getElementById('statusNote').value;

    fetch('/api/update_status',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            application_id: appToChange,
            new_status: newStatusValue,
            note: newNote
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Status was not updated");
        }
        return response.json();
    })
    .then(data =>{
        console.log(data.message)
        alert(data.message);

        
    })

    .catch(error =>{
        console.error('Error updating status:', error);
        alert("Error updating status.");

    });
}


function addDevice(){
    console.log("add device");

    const appEUI = document.getElementById("AppEUI").value;
    const appKey = document.getElementById("AppKey").value;
    const devEUI = document.getElementById("DevEUI").value;

    // Check if the DevEUI and AppEUI are in the correct format
    const regex = /^[0-9a-f]{16}$/;
    if (!regex.test(appEUI)) {
        alert("The AppEUI must be 16 characters long and contain only numbers and letters a-f.");
        return;
    }
    const reegex = /^[0-9a-f]{16}$/;
    if (!reegex.test(devEUI)) {
        alert("The DevEUI must be 16 characters long and contain only numbers and letters a-f.");
        return;
    }

    // Check if the AppKey is in the correct format
    const regeex = /^[0-9a-f]{32}$/;
    if (!regeex.test(appKey)) {
        alert("The AppKey must be 32 characters long and contain only numbers and letters a-f.");
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/device/add', true);
    
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onreadystatechange = () => { // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            
            console.log("Success")
            location.href = "peripherique.html";
        }
    }
    xhr.send(JSON.stringify({
        "AppEUI": appEUI,
        "AppKey": appKey,
        "DevEUI": devEUI
    }));
 
} 


function getDevices()
{
    console.log("get device")

    const xhr = new XMLHttpRequest();
    xhr.open("GET", '/device/all', true);
    
    
    xhr.onreadystatechange = () => { // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            
            console.log(JSON.parse(xhr.response))
        }
    }
    xhr.send(); 
}


function getSystem()
{

    const xhr = new XMLHttpRequest();
    xhr.open("GET", '/system', true);
    
    
    xhr.onreadystatechange = () => { // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            
            console.log(JSON.parse(xhr.response))
        }
    }
    xhr.send(); 
}

function generateRandomString(inputId, length) {
    var chars = '0123456789abcdef';
    var result = '';    
    var input = document.getElementById(inputId);  
    for (var i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }  
    input.value = result;
}
function deleteDevices() {
    var checkboxes = document.querySelectorAll("input[type=checkbox]:checked");
    var DevEUIs = [];

    checkboxes.forEach(function (checkbox)
 {
        DevEUIs.push(checkbox.getAttribute("data-dev-eui"));
    });

    if (DevEUIs.length > 0) {
        if (confirm("Are you sure you want to delete the selected devices?")) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/device/delete", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        location.reload();
                    } else {
                        alert("Failed to delete devices.");
                    }
                }
            };
            xhr.send(JSON.stringify({ "DevEUIs": DevEUIs }));
        }
    } else {
        alert("Please select at least one device to delete.");
    }
}


  
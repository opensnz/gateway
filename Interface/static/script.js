function addDevice(){
    console.log("add device")

    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/device/add', true);
    
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onreadystatechange = () => { // Call a function when the state changes.
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Request finished. Do processing here.
            
            console.log("Success")
        }
    }
    xhr.send(JSON.stringify({
        "AppEUI": "0000000000000000",
        "AppKey": "45abd993fa42864305fd20b63b21b80d",
        "DevEUI": "b53fcaaa8725fe11"
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

function random() {
    var length;
    var chars = '0123456789abcdefghijklmnopqrstuv';
    var result = '';
    
    var input = document.getElementById("AppEUI");
    if (input) {
      length = 16; // set length to 16 for AppEUI and DevEUI
    } else if (input = document.getElementById("DevEUI")) {
      
      length = 16; // set length to 32 for AppKey
    } else {
        length = 32;
    }
    
    for (var i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
  
    input.value = result;
  }
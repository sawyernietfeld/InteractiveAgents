function sendCommand() {
    var command = document.getElementById('user-command').value;
    //send command
    var updatesDiv = document.getElementById('agent-updates');
    updatesDiv.innerHTML += '<p><strong>You:</strong> ' + command + '</p>';


    // Send the command to the Flask server
    fetch('http://localhost:5000/send-command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        var updatesDiv = document.getElementById('agent-updates');
        updatesDiv.innerHTML += '<p><strong>Agent:</strong> ' + data.response + '</p>';
    })
    .catch(error => console.error('Error:', error));

    // Clear the textarea
    document.getElementById('user-command').value = '';
}
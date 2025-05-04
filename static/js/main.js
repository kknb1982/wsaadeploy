// Add new travel record
function submitTravel() {
    const travelData = {
        institution: document.getElementById('institution').value,
        city: document.getElementById('city').value,
        country: document.getElementById('country').value,
        travelstart: document.getElementById('departure_date').value,
        travelend: document.getElementById('return_date').value
    };

    fetch('/api/travel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(travelData)
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.message) {
            // Display success message
            messageDiv.style.color = 'green';
            messageDiv.textContent = 'Travel Successfully Added.';
        } else if (data.error) {
            // Display error message
            messageDiv.style.color = 'red';
            messageDiv.textContent = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        // Handle network or other errors
        const messageDiv = document.getElementById('message');
        messageDiv.style.color = 'red';
        messageDiv.textContent = `Error: ${error.message}`;
    });
}

function loadTravel() {
    fetch('/api/travel')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const travelList = document.getElementById('travelList');
        travelList.innerHTML = ''; // Clear any existing content

        if (data.length === 0) {
            travelList.innerHTML = '<p>No travel records found.</p>';
            return;
        }

        // Create a table element
        const table = document.createElement('table');
        table.setAttribute('border', '1'); 
        table.style.width = '100%'; 

        // Create the table header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Institution</th>
                <th>City</th>
                <th>Country</th>
                <th>Travel Start</th>
                <th>Travel End</th>
                <th>Actions</th>
            </tr>
        `;
        table.appendChild(thead);

        // Create the table body
        const tbody = document.createElement('tbody');
        data.forEach(travel => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${travel.institution}</td>
                <td>${travel.city}</td>
                <td>${travel.country}</td>
                <td>${travel.travelstart}</td>
                <td>${travel.travelend}</td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="window.location.href='/update-travel?id=${travel.travelid}'">Update</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        // Append the table to the travelList container
        travelList.appendChild(table);
    })
    .catch(error => {
        console.error('Error:', error);
        const travelList = document.getElementById('travelList');
        travelList.innerHTML = '<p>An error occurred while loading travel records. Please try again later.</p>';
    });
}

function submitUpdateTravel() {
    const travelData = {
        id: new URLSearchParams(window.location.search).get('id'), // Get the travel ID from the URL
        institution: document.getElementById('institution').value,
        city: document.getElementById('city').value,
        country: document.getElementById('country').value,
        travelstart: document.getElementById('travelstart').value,
        travelend: document.getElementById('travelend').value
    };

    fetch('/api/update-travel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(travelData)
    })
    .then(response => {
        if (response.ok) {
            alert('Travel record updated successfully!');
            window.location.href = '/view-travel'; // Redirect back to the travel list
        } else {
            alert('Failed to update travel record. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the travel record.');
    });
}

function submitUpdateUser() {
    // Use the currentUserId variable passed from the server
    const userId = currentUserId;

    const userData = {
        userid: userId, // Include the current user's ID
        firstname: document.getElementById('firstname').value,
        surname: document.getElementById('surname').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        role: document.getElementById('role').value
    };

    fetch('/api/user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (response.ok) {
            const formContainer = document.getElementById('updateUserFormContainer');
            formContainer.innerHTML = `
                <p style="color: green;">User record updated successfully!</p>
                <button onclick="window.location.href='/dashboard'" class="btn btn-primary">Back to Dashboard</button>
            `;
        } else {
            alert('Failed to update user record. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the user record.');
    });
}
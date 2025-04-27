// Add new travel record
function submitTravel() {
    const travelData = {
        name: document.getElementById('name').value,
        destination: document.getElementById('destination').value,
        departure_date: document.getElementById('departure_date').value,
        return_date: document.getElementById('return_date').value
    };

    fetch('/api/travel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(travelData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Travel Added!');
        window.location.href = '/view-travel';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function loadTravel() {
    fetch('/api/travel')
    .then(response => response.json())
    .then(data => {
        const travelList = document.getElementById('travelList');
        travelList.innerHTML = ''; // Clear any existing content

        // Create a table element
        const table = document.createElement('table');
        table.setAttribute('border', '1'); 
        table.style.width = '100%'; 

        // Create the table header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>First Name</th>
                <th>Surname</th>
                <th>Role</th>
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
                <td>${travel.firstname}</td>
                <td>${travel.surname}</td>
                <td>${travel.role}</td>
                <td>${travel.institution}</td>
                <td>${travel.city}</td>
                <td>${travel.country}</td>
                <td>${travel.travelstart}</td>
                <td>${travel.travelend}</td>
                <td> <button class="btn btn-primary btn-sm" onclick="updateTravel(${travel.id})">Update</button></td>
            `;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        // Append the table to the travelList container
        travelList.appendChild(table);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

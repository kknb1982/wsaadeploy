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

// All travel records 
function loadTravel() {
    fetch('/api/travel/${userid}')
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
                <td><a href="/country-details/${travel.country}" class="btn btn-link">${travel.country}</a></td>
                <td>${formatDateToDDMMYYYY(travel.travelstart)}</td>
                <td>${formatDateToDDMMYYYY(travel.travelend)}</td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="window.location.href='/update-travel/${travel.travelid}'">Update</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTravel(${travel.travelid})">Delete</button>
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

// Loads travel record for update
function loadTravelForUpdate(travelId) {
    fetch(`/api/travel/${travelId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
        }
            return response.json();
        })
        .then(travel => {
            document.getElementById('institution').value = data.institution;
            document.getElementById('city').value = data.city;
            document.getElementById('country').value = data.country;
            document.getElementById('travelstart').value = formatDateToDDMMYYYY(data.travelstart); // Format date to YYYY-MM-DD
            document.getElementById('travelend').value = formatDateToDDMMYYYY(data.travelend); // Format date to YYYY-MM-DD
        }) 
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while loading the travel record. Please try again later.');
        });
}

function submitUpdateTravel() {
    const travelData = {
        id: new URLSearchParams(window.location.search).get('id'), // Get the travel ID from the URL
        institution: document.getElementById('institution').value,
        city: document.getElementById('city').value,
        country: document.getElementById('country').value,
        travelstart: formatDateToDDMMYYYY(document.getElementById('travelstart').value),
        travelend: formatDateToDDMMYYYY(document.getElementById('travelend').value)
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
    const userId = window.location.pathname.split('/').pop();

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
        const messageDiv = document.getElementById('message'); 
        if (response.ok) {
            messageDiv.style.color = 'green';
            messageDiv.textContent = 'User record updated successfully!';

        } else {
            messageDiv.style.color = 'red';
            messageDiv.textContent = 'Failed to update user record. Please try again.';
            alert('Failed to update user record. Please try again.');
        }
    })
    .catch(error => {
        // Handle network or other errors
        const messageDiv = document.getElementById('message');
        messageDiv.style.color = 'red';
        messageDiv.textContent = `Error: ${error.message}`;
    });
}

function formatDateToDDMMYYYY(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}-${month}-${year}`;
}

function loadCurrentTravel() {
    fetch('/api/current-travel') // Fetch current travel data from the backend
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            travelData = data; // Store the data globally
            displayTravelData(travelData); // Display the data in the table
        })
        .catch(error => {
            console.error('Error:', error);
            const travelList = document.getElementById('travelList');
            travelList.innerHTML = '<p>An error occurred while loading travel records. Please try again later.</p>';
        });
}

// Display travel data in the table
function displayTravelData(data) {
    const travelTableBody = document.getElementById('travelTableBody');
    travelTableBody.innerHTML = ''; // Clear existing rows

    if (data.length === 0) {
        travelTableBody.innerHTML = '<tr><td colspan="8">No travel records found.</td></tr>';
        return;
    }

    data.forEach(travel => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${travel.travelid}</td>
            <td>${travel.userid}</td>
            <td>${travel.institution}</td>
            <td>${travel.city}</td>
            <td>${travel.country}</td>
            <td>${travel.travelstart}</td>
            <td>${travel.travelend}</td>
            <td>No news loaded</td> <!-- News column initially empty -->
        `;
        travelTableBody.appendChild(row);
    });
}

// Fetch incident news for current travel records
function loadIncidentNews() {
    if (travelData.length === 0) {
        alert('No travel records available to fetch news.');
        return;
    }

    // Fetch news for each travel record
    travelData.forEach(travel => {
        fetch(`/api/news?city=${encodeURIComponent(travel.city)}&country=${encodeURIComponent(travel.country)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(news => {
                // Add news to the travel record
                travel.news = news;
                displayTravelDataWithNews(travelData); // Update the table with news
            })
            .catch(error => {
                console.error(`Error fetching news for ${travel.city}, ${travel.country}:`, error);
            });
    });
}

// Display travel data with news in the table
function displayTravelDataWithNews(data) {
    const travelTableBody = document.getElementById('travelTableBody');
    travelTableBody.innerHTML = ''; // Clear existing rows

    data.forEach(travel => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${travel.travelid}</td>
            <td>${travel.userid}</td>
            <td>${travel.institution}</td>
            <td>${travel.city}</td>
            <td>${travel.country}</td>
            <td>${travel.travelstart}</td>
            <td>${travel.travelend}</td>
            <td>
                ${travel.news && travel.news.length > 0 ? `
                    <ul>
                        ${travel.news.map(news => `<li><a href="${news.url}" target="_blank">${news.title}</a></li>`).join('')}
                    </ul>
                ` : 'No incident news available'}
            </td>
        `;
        travelTableBody.appendChild(row);
    });
}
// Filter travel data based on user input
function filterTravel() {
    const cityFilter = document.getElementById('filterCity').value.toLowerCase();
    const countryFilter = document.getElementById('filterCountry').value.toLowerCase();
    const startDateFilter = document.getElementById('filterStartDate').value;
    const endDateFilter = document.getElementById('filterEndDate').value;

    const filteredData = travelData.filter(travel => {
        const matchesCity = travel.city.toLowerCase().includes(cityFilter);
        const matchesCountry = travel.country.toLowerCase().includes(countryFilter);
        const matchesStartDate = !startDateFilter || new Date(travel.travelstart) >= new Date(startDateFilter);
        const matchesEndDate = !endDateFilter || new Date(travel.travelend) <= new Date(endDateFilter);

        return matchesCity && matchesCountry && matchesStartDate && matchesEndDate;
    });

    displayTravelData(filteredData); // Update the table with filtered data
}

function loadCountryList() {
    fetch('/country-list')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const countryList = document.getElementById('countryList');
            countryList.innerHTML = ''; // Clear existing content
            if (data.error) {
                countryList.innerHTML = `<tr><td colspan="4">${data.error}</td></tr>`;
                return;
            }

            data.forEach(country => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${country.name}</td>
                    <td>${country.code}</td>
                    <td><a href="/country-details/${country.name}" class="btn btn-link">View Details</a></td>
                    <td>${country.fco_link ? `<a href="${country.fco_link}" target="_blank">FCO Link</a>` : 'N/A'}</td>
                `;
                countryList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading country list:', error);
            const countryList = document.getElementById('countryList');
            countryList.innerHTML = '<tr><td colspan="4">An error occurred while loading the country list. Please try again later.</td></tr>';
        });
}

function loginAsAdmin() {
    const userid = document.getElementById('userid').value;

    if (!userid) {
        alert('Please enter your User ID before logging in as an administrator.');
        return;
    }

    fetch(`/api/check-admin/${userid}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.isAdmin) {
                // Redirect to the admin dashboard
                window.location.href = `/admin-dashboard/${userid}`;
            } else {
                alert('You do not have administrator privileges.');
            }
        })
        .catch(error => {
            console.error('Error checking admin status:', error);
            alert('An error occurred while checking admin status. Please try again.');
        });
}


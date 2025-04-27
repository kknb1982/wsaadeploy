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

// Load all travel records
function loadTravel() {
    fetch('/api/travel')
    .then(response => response.json())
    .then(data => {
        const travelList = document.getElementById('travelList');
        travelList.innerHTML = '';

        data.forEach(travel => {
            const div = document.createElement('div');
            div.innerHTML = `
                <strong>${travel.name}</strong> to <em>${travel.destination}</em>
                from ${travel.departure_date} to ${travel.return_date}
                <hr>
            `;
            travelList.appendChild(div);
        });
    });
}

// Call loadTravel automatically if on view_travel.html
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('travelList')) {
        loadTravel();
    }
});

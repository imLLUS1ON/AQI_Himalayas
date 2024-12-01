document.getElementById('locationDropdown').addEventListener('change', function() {
    const selectedLocation = this.value;

    fetch(`/air_quality/${selectedLocation}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Update location and AQI
        document.getElementById('location').innerText = data.location;
        document.getElementById('aqi').innerText = data.AQI;

        // Update all components dynamically
        const details = data.details;
        document.getElementById('co').innerText = details.co || '-';
        document.getElementById('nh3').innerText = details.nh3 || '-';
        document.getElementById('no').innerText = details.no || '-';
        document.getElementById('no2').innerText = details.no2 || '-';
        document.getElementById('o3').innerText = details.o3 || '-';
        document.getElementById('pm10').innerText = details.pm10 || '-';
        document.getElementById('pm25').innerText = details.pm2_5 || '-';
        document.getElementById('so2').innerText = details.so2 || '-';
    })
    .catch(err => console.error('Error fetching data:', err));
});

// Trigger initial load
document.getElementById('locationDropdown').dispatchEvent(new Event('change'));
document.getElementById('locationDropdown').addEventListener('change', function () {
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

        // Ensure AQI (Indian Standard) is updated
        document.getElementById('aqi').innerText = data.AQI || "Data unavailable";

        // Update all components dynamically
        const details = data.details || {};
        document.getElementById('co').innerText = details.co || '-';
        document.getElementById('nh3').innerText = details.nh3 || '-';
        document.getElementById('no').innerText = details.no || '-';
        document.getElementById('no2').innerText = details.no2 || '-';
        document.getElementById('o3').innerText = details.o3 || '-';
        document.getElementById('pm10').innerText = details.pm10 || '-';
        document.getElementById('pm25').innerText = details.pm2_5 || '-';
        document.getElementById('so2').innerText = details.so2 || '-';

        // Update the background image based on the selected location
        const backgroundMap = {
            "Kedarnath": "/static/images/kedarnathbaba1.jpg",
            "Badrinath": "/static/images/badrinathbaba.jpg",
            "Rudranath": "/static/images/Rudranathbaba.jpg"
        };
        document.body.style.backgroundImage = `url(${backgroundMap[selectedLocation]})`;
    })
    .catch(err => console.error('Error fetching data:', err));

});

// Trigger the change event on page load to fetch data for the default location
document.getElementById('locationDropdown').dispatchEvent(new Event('change'));

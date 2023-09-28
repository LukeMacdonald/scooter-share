"use strict";

function initMap() {
    const myLatLng = {
        lat: -37.812374114990234,
        lng: 144.96246337890625
    };
    const map = new google.maps.Map(document.getElementById("gmp-map"), {
        zoom: 14,
        center: myLatLng,
        fullscreenControl: false,
        zoomControl: true,
        streetViewControl: false
    });

     const customIcon = {
        url: "https://cdn-icons-png.flaticon.com/512/1819/1819598.png",
        scaledSize: new google.maps.Size(32, 32)
    };

     // Check if scooterData is defined
     if (typeof scooterData !== 'undefined') {
        const customIcon = {
            url: "https://cdn-icons-png.flaticon.com/512/1819/1819598.png",
            scaledSize: new google.maps.Size(32, 32)
        };

        // Iterate over scooter data and create markers
        for (let i = 0; i < scooterData.length; i++) {
            const scooter = scooterData[i];
            new google.maps.Marker({
                position: { lat: scooter.Latitude, lng: scooter.Longitude },
                map,
                title: "Scooter ID: " + scooter.ScooterID,
                icon: customIcon
            });
        }
}


document.addEventListener("DOMContentLoaded", function () {
    const tableRows = document.querySelectorAll("tr[data-latitude][data-longitude]");
    const locateButtons = document.querySelectorAll(".locate-button");

    locateButtons.forEach(function (button, index) {
        button.addEventListener("click", function () {
            const row = tableRows[index]; // Get the corresponding table row
            const latitude = parseFloat(row.getAttribute("data-latitude"));
            const longitude = parseFloat(row.getAttribute("data-longitude"));
            const scooterLatLng = new google.maps.LatLng(latitude, longitude);
            map.panTo(scooterLatLng);
        });
    });
});
}
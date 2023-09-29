
// Majority of the below code was sourced from Google Maps Platform
// https://console.cloud.google.com/google/maps-apis/discover
"use strict";


let map, infoWindow;
let userLocation;

function initMap() {
    const defaultLocation = { lat: -37.81237, lng: 144.96246 };
    map = new google.maps.Map(document.getElementById("gmp-map"), {
        zoom: 14,
        center: defaultLocation,
        fullscreenControl: false,
        zoomControl: true,
        streetViewControl: false
    });
    infoWindow = new google.maps.InfoWindow();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                map.panTo(userLocation);

                const userLocationMarker = new google.maps.Marker({
                    position: userLocation,
                    map,
                    title: "Your Location",
                    icon: {
                        url: "https://cdn-icons-png.flaticon.com/512/9204/9204285.png",
                        scaledSize: new google.maps.Size(32, 32)
                    }
                });
            },
            () => handleLocationError(true, infoWindow, map.getCenter())
        );
    } else {
        handleLocationError(false, infoWindow, map.getCenter());
    }

    const locationButton = document.createElement("button");

    locationButton.textContent = "Current Location";
    locationButton.classList.add("btn", "btn-dark","current-location");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    
    /* CODE TO GET LAT AND LONG FROM CURRENT LOCATION */
    locationButton.addEventListener("click", () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    }; 
                    map.panTo(userLocation);
                },
                () => handleLocationError(true, infoWindow, map.getCenter())
            );
        } else {
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });

    const customIcon = {
        url: "https://cdn-icons-png.flaticon.com/512/1819/1819598.png",
        scaledSize: new google.maps.Size(32, 32)
    };

    if (typeof scooterData !== 'undefined') {
        for (const scooter of scooterData) {
            new google.maps.Marker({
                position: { lat: scooter.Latitude, lng: scooter.Longitude },
                map,
                title: `Scooter ID: ${scooter.ScooterID}`,
                icon: customIcon
            });
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        const tableRows = document.querySelectorAll("tr[data-latitude][data-longitude]");
        const locateButtons = document.querySelectorAll(".locate-button");
        const directionButtons = document.querySelectorAll(".direction-button");

        locateButtons.forEach(function (button, index) {
            button.addEventListener("click", function () {
                const row = tableRows[index];
                const latitude = parseFloat(row.getAttribute("data-latitude"));
                const longitude = parseFloat(row.getAttribute("data-longitude"));
                const scooterLatLng = new google.maps.LatLng(latitude, longitude);
                map.panTo(scooterLatLng);
            });
        });

        directionButtons.forEach(function (button,index) {
            button.addEventListener("click", function () {
                const row = tableRows[index];
                const latitude = parseFloat(row.getAttribute("data-latitude"));
                const longitude = parseFloat(row.getAttribute("data-longitude")); 
                const scooterLatLng = new google.maps.LatLng(latitude, longitude);
                if (userLocation) {
                    calculateAndDisplayRoute(userLocation, scooterLatLng);
                } else {
                    window.alert("User location not available.");
                }
            });
        });
    })
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

function calculateAndDisplayRoute(origin, destination) {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true, // Prevent default markers on the route
        panel: document.getElementById('directions-panel') // Display directions in an HTML element
    });

    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING
    };

    directionsService.route(request, function (response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(response);
        } else {
            window.alert("Directions request failed due to " + status);
        }
    });
}

window.initMap = initMap;
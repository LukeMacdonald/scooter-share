"use strict";

let map, infoWindow;
let userLocation;
const defaultLocation = { lat: -37.81237, lng: 144.96246 };

function initMap() {
    setupMap();
    setupCurrentLocationButton();
    setupScooterMarkers();
    setupEventListeners();

    getUserLocation()
        .then((location) => {
            userLocation = location;
            map.panTo(userLocation);
            addCurrentUserMarker(userLocation);
        })
        .catch((error) => {
            console.error("Error getting location:", error);
            handleLocationError(true, infoWindow, map.getCenter());
        });
}

function setupMap() {
    
    map = new google.maps.Map(document.getElementById("gmp-map"), {
        zoom: 14,
        center: defaultLocation,
        fullscreenControl: false,
        zoomControl: true,
        streetViewControl: false
    });
    infoWindow = new google.maps.InfoWindow();
}

function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const location = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    resolve(location);
                },
                (error) => {
                    reject(error);
                }
            );
        } else {
            reject("Geolocation not supported");
        }
    });
}

function setupCurrentLocationButton() {
    const locationButton = document.createElement("button");
    locationButton.textContent = "Current Location";
    locationButton.classList.add("btn", "btn-dark", "current-location");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

    locationButton.addEventListener("click", () => {
        getUserLocation()
            .then((location) => {
                userLocation = location;
                map.panTo(userLocation);
            })
            .catch((error) => {
                console.error("Error getting location:", error);
                handleLocationError(true, infoWindow, map.getCenter());
            });
    });
}

function setupScooterMarkers() {
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
}

function addCurrentUserMarker(location) {
    new google.maps.Marker({
        position: location,
        map: map,
        title: "Your Location",
        icon: {
            url: "https://cdn-icons-png.flaticon.com/512/9204/9204285.png",
            scaledSize: new google.maps.Size(32, 32)
        }
    });
}

function setupEventListeners() {
    document.addEventListener("DOMContentLoaded", function () {
        // Get data from html table
        const tableRows = document.querySelectorAll("tr[data-latitude][data-longitude]");
        const locateButtons = document.querySelectorAll(".locate-button");
        const directionButtons = document.querySelectorAll(".direction-button");

        // Event Listener for panning screen to scooter location
        locateButtons.forEach(function (button, index) {
            button.addEventListener("click", function () {
                const row = tableRows[index];
                const latitude = parseFloat(row.getAttribute("data-latitude"));
                const longitude = parseFloat(row.getAttribute("data-longitude"));
                const scooterLatLng = new google.maps.LatLng(latitude, longitude);
                map.panTo(scooterLatLng);
            });
        });
        // Event Listener for getting directions from users location to scooter
        directionButtons.forEach(function (button, index) {
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
    });
}

function handleLocationError(browserHasGeolocation, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

function calculateAndDisplayRoute(origin, destination) {
    // 
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true,
        // Option to display directions on html screen (currenty disabled)
        panel: document.getElementById('directions-panel')
    });

    const request = {
        origin: new google.maps.LatLng(origin.lat, origin.lng),
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
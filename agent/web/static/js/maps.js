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

    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "My location",
        icon: customIcon
    });

    new google.maps.Marker({
        position: {lat:-37.86616061413071, lng: 144.6228517415038 },
        map,
        title: "Pin 2",
        icon: customIcon
    });
}
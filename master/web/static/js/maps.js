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
    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "My location"
    });
}
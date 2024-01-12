

export const findOnMap = (mapRef, longitude, latitude) => {
    
    const location = { lat: latitude, lng: longitude };
    
    const zoomLevel = 15
  
    mapRef.current.panTo(location, {animate: true});

    mapRef.current.setZoom(zoomLevel, { animate: true });
    
};

export const routeTo = ( origin, destination, mapRef) => {

    const directionsService = new window.google.maps.DirectionsService();
    const directionsRenderer = new window.google.maps.DirectionsRenderer({
        map: mapRef.current,
        suppressMarkers: true,
        // Option to display directions on html screen (currenty disabled)
        panel: document.getElementById('directions-panel')
    });

    const request = {
        origin: new window.google.maps.LatLng(origin.lat, origin.lng),
        destination: destination,
        travelMode: window.google.maps.TravelMode.DRIVING
    };

    directionsService.route(request, function (response, status) {
        if (status === window.google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(response);
        } else {
            window.alert("Directions request failed due to " + status);
        }
    });
}
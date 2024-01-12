import React, { useEffect, useState, useRef } from 'react';
import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";
import useGeolocation from '../hooks/useGeolocation'; 
import { useMarkerMapping } from '../hooks/useMarkerMapping';

const MapComponent = ({ scooters, className, mapRef, centerRef }) => {
  
  const [markers, setMarkers] = useState([]);

  const { center, error: geolocationError } = useGeolocation();
  
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: 'AIzaSyCI9KBPlHOzx9z7dp41LNbzpYaVn3qqgNY',
  });

  const customIcon = isLoaded ? { url: "https://cdn-icons-png.flaticon.com/512/1819/1819598.png", scaledSize: new window.google.maps.Size(50, 50) } : null;
  const customUserIcon = isLoaded ? { url: "https://cdn-icons-png.flaticon.com/512/9204/9204285.png", scaledSize: new window.google.maps.Size(50, 50) } : null;

  const markerMapping = useMarkerMapping(scooters, customIcon);

  useEffect(() => {
    setMarkers(markerMapping);
  }, [scooters]);

  const onLoad = (map) => {
    mapRef.current = map; // Save the map instance to the ref
    const bounds = new window.google.maps.LatLngBounds();
    markers.forEach(({ lat, lng }) => bounds.extend(new window.google.maps.LatLng(lat, lng)));
    
    map.fitBounds(bounds);
  };

  useEffect(() => {
    // Check if the center is set and the map is loaded
    if (center && isLoaded) {
      mapRef.current.panTo(center); // Pan the map to the center
    }
  }, [center, isLoaded]);

  return (
    <div className={className}>
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : loadError ? (
        <div>Error loading map: {loadError}</div>
      ) : (
        <GoogleMap mapContainerClassName='w-full h-full rounded-lg' center={center} zoom={10} onLoad={onLoad}>
          {geolocationError ? (
            <div>Error obtaining location: {geolocationError}</div>
          ) : (
            <>
              {markers.map((marker, index) => (
                <Marker key={index} position={marker} icon={marker.icon} />
              ))}
              {center && <Marker position={center} icon={customUserIcon} />}
            </>
          )}
        </GoogleMap>
      )}
    </div>
  );
};

export default MapComponent;








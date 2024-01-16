import React, {useRef, useState, useEffect } from 'react'
import MapComponent from '../../components/Map'
import { useParams } from 'react-router-dom';
import { scooterData } from '../../api/api';
import { routeTo } from '../../api/google';
import useGeolocation from '../../hooks/useGeolocation';

const RouteTo = () => {
    
    const mapRef = useRef(null);
    
    const { center } = useGeolocation();
    
    const [scooter, setScooter] = useState([]);
  
    const { scooterID } = useParams();
  
    useEffect(() => {
      const fetchScooter = async () => {
        try {
          const scooter = await scooterData(scooterID);
          setScooter([scooter]);
        } catch (error) {
          console.error("Error fetching scooter data:", error);
        }
      };
  
      fetchScooter();
    }, [scooterID]);
  
    useEffect(() => {
      if (scooter.length > 0 && center) {
        console.log(center, scooter[0])
        routeTo(center, { lat: scooter[0].latitude, lng: scooter[0].longitude }, mapRef);
      }
   
    }, [scooter, center]);
  
    return (
      <MapComponent className='w-full h-full p-10' scooters={scooter} mapRef={mapRef} center={center} />
    );
  };
  
  export default RouteTo;
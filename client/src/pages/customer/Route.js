import React, {useRef, useState, useEffect } from 'react'
import MapComponent from '../../components/Map'
import { useParams } from 'react-router-dom';
import { scooterData } from '../../api/api';
import { routeTo } from '../../api/google';

const RouteTo = () => {
    
    const mapRef = useRef(null);
    
    const centerRef = useRef(null);
    
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
      if (scooter.length > 0 && centerRef.current) {
        console.log(scooter[0], centerRef.current)
        routeTo(centerRef.current, { lat: scooter[0].latitude, lng: scooter[0].longitude }, mapRef);
      }
      console.log(scooter[0], centerRef.current)
    }, [scooter, centerRef]);
  
    return (
      <MapComponent className='w-full h-full p-10' scooters={scooter} mapRef={mapRef} centerRef={centerRef} />
    );
  };
  
  export default RouteTo;
import {useState, useEffect} from 'react'
import { customerData } from '../api/api'

const useCustomerData = () => {
    
    const [scooters, setScooters] = useState([])
    const [bookings, setBookings] = useState([])

    const fetchData = async () => {
        try {
          const { scooters, bookings } = await customerData();
          setScooters(scooters);
          setBookings(bookings);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
    
      useEffect(() => {
        fetchData();
      }, []);

  return {scooters, bookings}
}

export default useCustomerData
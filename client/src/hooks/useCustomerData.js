import {useState, useEffect} from 'react'
import { customerData } from '../api/api'

const useCustomerData = () => {
    
    const [scooters, setScooters] = useState([])
    const [bookings, setBookings] = useState([])
    const [user, setUser] = useState({})

    const fetchData = async () => {
        try {
          const { scooters, bookings, user_details } = await customerData();
          setScooters(scooters);
          setBookings(bookings);
          setUser(user_details);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
    
      useEffect(() => {
        fetchData();
      }, []);

  return {scooters, bookings, user}
}

export default useCustomerData
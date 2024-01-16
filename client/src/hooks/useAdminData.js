import {useState, useEffect} from 'react'
import { adminData, } from '../api/api'

const useAdminData = () => {
    
    const [scooters, setScooters] = useState([])

    const [customers, setCustomers] = useState([])

    const fetchData = async () => {
        try {
          const { customers, scooters } = await adminData();
          console.log(customers)
          setScooters(scooters);
          setCustomers(customers);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
    
      useEffect(() => {
        fetchData();
      }, []);

  return {scooters, customers}
}

export default useAdminData
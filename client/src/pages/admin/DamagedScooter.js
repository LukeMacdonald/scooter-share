import React, { useEffect, useState, useRef } from 'react'
import MapComponent from '../../components/Map'
import { getReportedScooters, markScooterRepair } from '../../api/api'
import useGeolocation from '../../hooks/useGeolocation';
import { findOnMap } from '../../api/google';


const DamagedScooterDetails = ({repair, mapRef}) =>{


    const handleConfirm = async () => {
        await markScooterRepair({'repair_id': repair.repair_id})
        window.location.reload();
    }
  
    return(
      <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
        <td className='px-6 py-4'>{repair.scooter_id}</td>
        <td className='px-6 py-4'>{repair.report}</td>
        <td className='px-6 py-4'>
          <button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, repair.longitude, repair.latitude, 20)}>Locate</button>
        </td>
        <td className='px-6 py-4'><button className='text-orange-700 hover:underline font-semibold' onClick={()=>handleConfirm()}>Mark For Repair</button></td>

     
      </tr>
  
    )
  }
const DamagedScooter = () => {

    const [repairs, setRepairs] = useState([]);

    const {center} = useGeolocation()

    const mapRef = useRef(null);

    useEffect(()=>{
        const fetchScooters = async() => {
            const response = await getReportedScooters();
            setRepairs(response.repairs);            
        };
        fetchScooters();
    },[])
  return (
    <>
        <MapComponent className='w-full h-2/3 p-10' scooters={repairs} mapRef={mapRef} center={center} />
        <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold pb-3'>Pending Scooters</h1>
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">Scooter ID</th>
                <th scope="col" className="px-6 py-3">Repair Report</th>
                <th scope="col" className="px-6 py-3"></th>
                <th scope="col" className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody>
            {repairs.map((repair, index) => (
                <DamagedScooterDetails key={index} repair={repair} mapRef={mapRef}/>
              ))}
            </tbody>
          </table>
        </div>
        </>
  )
}

export default DamagedScooter;
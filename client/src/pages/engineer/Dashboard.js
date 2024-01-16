import React, { useEffect, useState, useRef } from "react"
import { Outlet } from "react-router-dom"
import { EngineerSidebar } from "../../components/Sidebar"
import { engineerData, reportRepair } from "../../api/api"
import useGeolocation from "../../hooks/useGeolocation"
import MapComponent from "../../components/Map"
import { findOnMap } from "../../api/google"
import { ViewReportModal } from "../../components/Modal"




const ReportedScooter = ({scooter, mapRef}) =>{
  
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
      setOpen(true);

  };

  const handleClose = () => {
      setOpen(false);
  };

  const handleReportRepair = async () => {
    
    await reportRepair({'scooter_id': scooter.scooter_id, 'repair_id': scooter.repair_id})
    
    window.location.reload()
  }

  return(
    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
      <td className='px-6 py-4'>{scooter.scooter_id}</td>
      <td className='px-6 py-4'>{scooter.make} ({scooter.colour})</td>
      <td className='px-6 py-4'>{scooter.remaining_power} %</td>
      <td className='px-6 py-4'>
        <button className='text-green-700 hover:underline font-semibold' onClick={handleOpen}>View</button>
      </td>
      <td className='px-6 py-4'>
        <button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}>Locate</button>
      </td>
      <td className='px-6 py-4'>
        <butoon 
          className='text-orange-700 hover:underline font-semibold' 
          onClick={handleReportRepair}
        >
          Fixed
        </butoon>
      </td>
      <ViewReportModal handleClose={handleClose} open={open} value={scooter.repair_report}/>
    </tr>

  )
}

export const EngineerLayout = ({children}) => {

    return(
      <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
        <div className='w-full h-full flex items-start justify-center'>
          <EngineerSidebar/>
          <div className='w-full h-full'>
            <Outlet/>
          </div>
        </div>
      </main>
    )
}

export const EngineerDashboard = () => {
    const [scooters, setScooters] = useState([])

    const mapRef = useRef(null);
  
    const { center } = useGeolocation();



    useEffect(()=>{
      const fetchScooters = async () =>{
        const scooters = await engineerData()
        setScooters(scooters);
      }

      fetchScooters()
      
    },[])

  
    return (
      <>
        <MapComponent className='w-full h-2/3 p-10' scooters={scooters} mapRef={mapRef} center={center} />
        
        <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold'>Scooters Needing Repair</h1>
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">Scooter ID</th>
                <th scope="col" className="px-6 py-3">Description</th>
                <th scope="col" className="px-6 py-3">Remaining Power</th>
                <th scope="col" className="px-6 py-3">Maintenance Details</th>
                <th scope="col" className="px-6 py-3"></th>
                <th scope="col" className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {scooters.map((scooter, index) => (
                <ReportedScooter key={index} scooter={scooter} mapRef={mapRef}/>
              ))}
            </tbody>
          </table>
          
          </div>
      </>
    )
  }
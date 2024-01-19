import React, { useEffect, useState, useRef } from "react"
import { Outlet, useNavigate } from "react-router-dom"
import { EngineerSidebar } from "../../components/Sidebar"
import { engineerData, reportRepair } from "../../api/api"
import useGeolocation from "../../hooks/useGeolocation"
import MapComponent from "../../components/Map"
import { findOnMap } from "../../api/google"
import { ViewReportModal } from "../../components/Modal"
import { useAuth } from "../../context/AuthContext"
import { getBatteryIcon, getPowerColor } from "../../components/utils/utils"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'



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
    <div className="bg-white space-y-4 p-4 rounded-lg shadow">
    <div className="flex items-center space-x-4 text-lg">
    <div className="font-bold hover:underline">{scooter.scooter_id}</div>
    <div>{scooter.make} ({scooter.colour})</div>
    <div>
        <span className={`p-1.5 text-sm font-medium uppercase tracking-wider text-dark-800 ${getPowerColor(scooter.remaining_power)} rounded-lg bg-opacity-50`}>
          {scooter.remaining_power}% {getBatteryIcon(scooter.remaining_power)}
        </span>
      </div>
    </div>
    <div className="flex items-center space-x-7 text-2xl">
      <div><button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}><FontAwesomeIcon icon={icon({name: 'map-location-dot'})} /></button></div>
      <div><button className='text-green-700 hover:underline font-semibold' onClick={handleOpen}><FontAwesomeIcon icon={icon({name: 'circle-info'})} /></button></div>
      <div>
        <butoon 
          className='text-orange-700 hover:underline font-semibold' 
          onClick={handleReportRepair}
        >
          <FontAwesomeIcon icon={icon({name: 'wrench'})} />
     
        </butoon>
      </div> 
    </div>
    <ViewReportModal handleClose={handleClose} open={open} value={scooter.repair_report}/>
  </div>
  )
}

export const EngineerLayout = ({children}) => {

  const { handleLogout, isLoggedIn, authUser } = useAuth();

  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn || authUser === null) {
      handleLogout();
      navigate("/");
    }
    if (isLoggedIn && authUser.role !== 'engineer'){
      navigate(`/${authUser.role}`);
    }
    
  },);

    return(
      <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
      <div className='w-full h-full flex md:flex-col items-start justify-between'>
          <EngineerSidebar/>
          <div className='w-5/6 md:w-full h-full'>
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
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 border overflow-y-auto max-h-[30rem] p-2">
          {scooters.map((scooter, index) => (
                <ReportedScooter key={index} scooter={scooter} mapRef={mapRef}/>
              ))}
          </div>          
          </div>
      </>
    )
  }
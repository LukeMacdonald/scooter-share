import React, { useRef, useEffect } from 'react'
import { Sidebar } from '../../components/Sidebar'
import MapComponent from '../../components/Map'
import { findOnMap } from '../../api/google'
import { Outlet, useNavigate } from 'react-router-dom'
import useCustomerData from '../../hooks/useCustomerData'
import useGeolocation from '../../hooks/useGeolocation'
import { useAuth } from '../../context/AuthContext'
import { getStatusColor, getBatteryIcon, getPowerColor } from "../../components/utils/utils"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'


export const ScooterDetails =  ({scooter, mapRef}) => {
  return(
    <div className="bg-white space-y-4 p-4 rounded-lg shadow">
      <div className="flex items-center space-x-4 text-md">
      <div className="font-bold hover:underline">{scooter.scooter_id}</div>
      <div>{scooter.make} ({scooter.colour})</div>
      <div>
          <span className={`p-1.5 text-xs font-medium uppercase tracking-wider text-dark-800 ${getPowerColor(scooter.remaining_power)} rounded-lg bg-opacity-50`}>
            {scooter.remaining_power}% {getBatteryIcon(scooter.remaining_power)}
          </span>
        </div>
      </div>
      <div className="text-gray-700 whitespace-nowrap text-sm">${scooter.cost_per_time} (per hour)</div>
      <div>                      
        <div class="flex items-center uppercase text-sm">
            <div className={`h-2.5 w-2.5 rounded-full ${getStatusColor(scooter.status)} me-2`}></div> {scooter.status}
        </div>
      </div>
      <div className="flex items-center space-x-10 text-xl">
        <div><button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}><FontAwesomeIcon icon={icon({name: 'map-location-dot'})} /></button></div>
        <div> <a className='text-green-700 hover:underline font-semibold' href={`customer/booking/${scooter.scooter_id}`}><FontAwesomeIcon icon={icon({name: 'calendar-check'})} /></a></div>
      </div>
    </div>
  )
}


export const CustomerLayout = ({children}) => {

  return(
    <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
       <div className='w-full h-full flex md:flex-col items-start justify-between'>
        <Sidebar/>
        <div className='w-5/6 md:w-full h-full'>
          <Outlet/>
        </div>
      </div>
    </main>
  )
}

export const CustomerDashboard = () => {
  const {scooters} = useCustomerData();

  const mapRef = useRef(null);
  
  const { center } = useGeolocation();

  const { handleLogout, isLoggedIn, authUser } = useAuth();
  
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn || authUser === null) {
      handleLogout();
      navigate("/");
    }
    if (isLoggedIn && authUser.role !== 'customer'){
      navigate(`/${authUser.role}`);
    }
    
  });

  return (
    <>
      
      <MapComponent className='w-full h-2/3 p-10' scooters={scooters} mapRef={mapRef} center={center} />
          <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold'>Available Scooters</h1>
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 border overflow-y-auto max-h-[30rem] p-2">
            {scooters.map((scooter, index) => (
                <ScooterDetails key={index} scooter={scooter} mapRef={mapRef}/>
              ))}
          </div>          
          </div>
    </>
  )
}
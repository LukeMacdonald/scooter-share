import React, { useRef, useEffect } from 'react'
import { Sidebar } from '../../components/Sidebar'
import MapComponent from '../../components/Map'
import { findOnMap } from '../../api/google'
import { Outlet, useNavigate } from 'react-router-dom'
import useCustomerData from '../../hooks/useCustomerData'
import useGeolocation from '../../hooks/useGeolocation'
import { useAuth } from '../../context/AuthContext'


export const CustomerLayout = ({children}) => {

  return(
    <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
      <div className='w-full h-full flex items-start justify-center'>
        <Sidebar/>
        <div className='w-full h-full'>
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
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">Scooter ID</th>
                <th scope="col" className="px-6 py-3">Description</th>
                <th scope="col" className="px-6 py-3">Cost Per Minute</th>
                <th scope="col" className="px-6 py-3"></th>
                <th scope="col" className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {scooters.map((scooter, index) => (
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">

              <td className='px-6 py-4'>{scooter.scooter_id}</td>
              <td className='px-6 py-4'>{scooter.make} ({scooter.colour})</td>
              <td className='px-6 py-4'>{scooter.cost_per_time}</td>
              <td className='px-6 py-4'>
              <button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}>Locate</button>
              </td>
              <td className='px-6 py-4'><a className='text-green-700 hover:underline font-semibold' href={`customer/booking/${scooter.scooter_id}`}>Book</a></td>
              </tr>
          ))}
              
          
            </tbody>
          </table>
          
          </div>

    </>
  )
}
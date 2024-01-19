import React, { useRef, useEffect } from "react"
import { Outlet, useNavigate } from "react-router-dom"
import { AdminSidebar } from "../../components/Sidebar"
import useGeolocation from "../../hooks/useGeolocation"
import useAdminData from "../../hooks/useAdminData"
import { findOnMap } from "../../api/google"
import MapComponent from "../../components/Map"
import { deleteCustomer, deleteScooter } from "../../api/api"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'
import { useAuth } from "../../context/AuthContext"
import { getStatusColor, getBatteryIcon, getPowerColor } from "../../components/utils/utils"


export const AdminLayout = ({ children }) => {
  const { setAuthUser, setIsLoggedIn, isLoggedIn, authUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn || authUser === null) {
      setIsLoggedIn(false);
      setAuthUser(null);
      navigate("/");
    }
    if (isLoggedIn && authUser.role !== 'admin'){
      navigate(`/${authUser.role}`);
    }

  });

  return (
    <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
      <div className='w-full h-full flex md:flex-col items-start justify-between'>
        <AdminSidebar />
        <div className='w-5/6 md:w-full h-full'>
          <Outlet />
        </div>
      </div>
    </main>
  );
};


export const CustomerDetails =  ({customer}) => {
  const navigate = useNavigate();

  const handleDelete = async (id) =>{

    await deleteCustomer(id);

    window.location.reload();

  }

  const handleEdit = async (id) => {
    navigate(`/admin/edit/customer/${id}`);
  }

  return(
    <div className="bg-white space-y-4 p-4 rounded-lg shadow">
      <div className="flex items-center space-x-8 text-md font-medium">
        <div className="font-bold hover:underline">{customer.id}</div>
        <div className=''>{customer.first_name} {customer.last_name}</div>
       
      </div>
      <div className="flex items-center space-x-8">
        <div className="flex items-center justify-start space-x-2">
          <FontAwesomeIcon icon={icon({ name: 'envelope'})}/>
          <p>{customer.email}</p> 
        </div>
        <div className="flex items-center justify-start space-x-2">
          <FontAwesomeIcon icon={icon({ name: 'phone'})}/>
          <p>{customer.phone_number}</p> 
        </div>
      </div>
      <p className="font-medium">Balance: <span className="font-normal">$ {customer.balance}</span></p>
      <div className="flex items-center space-x-7 text-xl">
        <div><button className='text-red-700 hover:underline font-semibold' onClick={()=>handleDelete(customer.id)}><FontAwesomeIcon icon={icon({ name: 'trash'})}/></button></div>
        <div><button className='text-gray-400 hover:underline font-semibold' onClick={()=>handleEdit(customer.id)}><FontAwesomeIcon icon={icon({ name: 'edit'})}/></button></div>
      </div>
    </div>
  )
}

export const ScooterDetails =  ({scooter, mapRef}) => {
  const navigate = useNavigate();

  const handleDelete = async (id) =>{

    await deleteScooter(id);

    window.location.reload();

  }

  const handleEdit = async (id) => {
    navigate(`/admin/edit/scooter/${id}`);
  }

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
      <div className="flex items-center space-x-7 text-lg">
        <div><button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}><FontAwesomeIcon icon={icon({name: 'map-location-dot'})} /></button></div>
        <div><button className='text-red-700 hover:underline font-semibold' onClick={()=>handleDelete(scooter.scooter_id)}><FontAwesomeIcon icon={icon({name: 'trash'})} /></button></div>
        <div><button className='text-gray-400 hover:underline font-semibold pl-2' onClick={()=>handleEdit(scooter.scooter_id)}><FontAwesomeIcon icon={icon({name: 'edit'})} /></button></div>
        <div> <a className='text-purple-700 hover:underline font-semibold' href={`/admin/scooter/qr/${scooter.scooter_id}`}><FontAwesomeIcon icon={icon({name: 'qrcode'})} /></a></div>
      </div>
    </div>
  )
}

export const AdminDashboard = () => {

    const {scooters, customers} = useAdminData();

    const mapRef = useRef(null);
  
    const { center } = useGeolocation();

    const navigate = useNavigate();

    const handleAdd = () => {
      navigate('/admin/add/scooter');
    }

    return (
        <>
        <MapComponent className='w-full h-2/3 p-10' scooters={scooters} mapRef={mapRef} center={center} />
        
        <div className='w-full p-10 !pt-0'>
          <div className="w-full flex items-center justify-between pr-5 pb-2">
            <h1 className='text-2xl font-semibold pb-3'>Scooters</h1>
            <button className='bg-primary p-2 px-4 rounded-md text-light hover:underline font-semibold ' onClick={()=>handleAdd()}>
            <FontAwesomeIcon icon={icon({name: 'plus'})} />
            </button>

          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 border overflow-y-auto max-h-[30rem] p-2">
            {scooters.map((scooter, index) => (
                <ScooterDetails key={index} scooter={scooter} mapRef={mapRef}/>
              ))}
          </div>

          
          </div>
          <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold pb-3'>Customers</h1>
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 border overflow-y-auto max-h-[30rem] p-2">
          {customers.map((customer, index) => (
                <CustomerDetails key={index} customer={customer}/>
              ))}
          </div>
          </div>
        
      </>
    )
  
}
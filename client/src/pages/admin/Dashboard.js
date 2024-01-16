import React, { useRef } from "react"
import { Outlet, useNavigate } from "react-router-dom"
import { AdminSidebar } from "../../components/Sidebar"
import useGeolocation from "../../hooks/useGeolocation"
import useAdminData from "../../hooks/useAdminData"
import { findOnMap } from "../../api/google"
import MapComponent from "../../components/Map"
import { deleteCustomer, deleteScooter } from "../../api/api"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from "@fortawesome/fontawesome-svg-core"


const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'bg-green-500'; // Green color for 'active'
      case 'awaiting repair':
        return 'bg-red-500'; // Red color for 'cancelled'
      case 'occupying':
        return 'bg-blue-500'; // Blue color for 'completed'
      default:
        return 'bg-gray-500'; // Default color (gray) for other statuses
    }
};

const ScooterDetails = ({scooter, mapRef}) =>{

    const navigate = useNavigate();

    const handleDelete = async (id) =>{

      await deleteScooter(id);

      window.location.reload();

    }

    const handleEdit = async (id) => {
      navigate(`/admin/edit/scooter/${id}`);
    }
  
    return(
      <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
        <td className='px-6 py-4'>{scooter.scooter_id}</td>
        <td className='px-6 py-4'>{scooter.make} ({scooter.colour})</td>
        <td className='px-6 py-4'>$ {scooter.cost_per_time}</td>
        <td className='px-6 py-4'>{scooter.remaining_power} %</td>
        <td className='px-6 py-4'>
                        <div class="flex items-center">
                            <div className={`h-2.5 w-2.5 rounded-full ${getStatusColor(scooter.status)} me-2`}></div> {scooter.status}
                        </div>
                    </td>
        
        <td className='px-6 py-4'>
          <button className='text-blue-700 hover:underline font-semibold' onClick={() => findOnMap(mapRef, scooter.longitude, scooter.latitude, 20)}>Locate</button>
        </td>
        <td className='px-6 py-4'><button className='text-red-700 hover:underline font-semibold' onClick={()=>handleDelete(scooter.scooter_id)}>Remove</button></td>
        <td className='px-6 py-4'><button className='text-gray-400 hover:underline font-semibold' onClick={()=>handleEdit(scooter.scooter_id)}>Edit</button></td>
     
      </tr>
  
    )
  }
  const CustomerDetails = ({customer}) =>{

    const navigate = useNavigate();

    const handleDelete = async (id) =>{

      await deleteCustomer(id);

      window.location.reload();

    }

    const handleEdit = async (id) => {
      navigate(`/admin/edit/customer/${id}`);
    }
  
    return(
      <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
        <td className='px-6 py-4'>{customer.id}</td>
        <td className='px-6 py-4'>{customer.first_name} {customer.last_name}</td>
        <td className='px-6 py-4'>{customer.username}</td>
        <td className='px-6 py-4'>{customer.email}</td>
        <td className='px-6 py-4'>{customer.phone_number}</td>
        <td className='px-6 py-4'>$ {customer.balance}</td>
        <td className='px-6 py-4'><button className='text-red-700 hover:underline font-semibold' onClick={()=>handleDelete(customer.id)}>Remove</button></td>
        <td className='px-6 py-4'><button className='text-gray-400 hover:underline font-semibold' onClick={()=>handleEdit(customer.id)}>Edit</button></td>
      </tr>
  
    )
  }

export const AdminLayout = ({children}) => {

    return(
      <main className='w-full h-screen max-h-screen flex flex-col justify-start items-start'>
        <div className='w-full h-full flex items-start justify-center'>
          <AdminSidebar/>
          <div className='w-full h-full'>
            <Outlet/>
          </div>
        </div>
      </main>
    )
}

export const AdminDashboard = () => {

    const {scooters, customers} = useAdminData();

    const mapRef = useRef(null);
  
    const { center } = useGeolocation();

    const navigate = useNavigate();

    console.log(scooters)

    const handleAdd = () => {
      navigate('/admin/add/scooter');
    }


  
    return (
        <>
        <MapComponent className='w-full h-2/3 p-10' scooters={scooters} mapRef={mapRef} center={center} />
        
        <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold pb-3'>Scooters</h1>
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">Scooter ID</th>
                <th scope="col" className="px-6 py-3">Description</th>
                <th scope="col" className="px-6 py-3">Cost (per hour)</th>
                <th scope="col" className="px-6 py-3">Remaining Power</th>
                <th scope="col" className="px-6 py-3">Status</th>
                <th scope="col" className="px-6 py-3 col-span-4"></th>
                <th scope="col" className="px-6 py-3 text-center mx-auto">
                  <button className='text-green-600 hover:underline font-semibold ' onClick={()=>handleAdd()}>
                    Add
                  </button>
                </th>
                <th scope="col" className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {scooters.map((scooter, index) => (
                <ScooterDetails key={index} scooter={scooter} mapRef={mapRef}/>
              ))}
            </tbody>
          </table>
          
          </div>
          <div className='w-full p-10 !pt-0'>
          <h1 className='text-xl font-semibold pb-3'>Customers</h1>
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">ID</th>
                <th scope="col" className="px-6 py-3">Name</th>
                <th scope="col" className="px-6 py-3">Username</th>
                <th scope="col" className="px-6 py-3">Email</th>
                <th scope="col" className="px-6 py-3">Phone Number</th>
                <th scope="col" className="px-6 py-3">Balance</th>
                <th scope="col" className="px-6 py-3"></th>
                <th scope="col" className="px-6 py-3"></th>
                
              </tr>
            </thead>
            <tbody>
              {customers.map((customer, index) => (
                <CustomerDetails key={index} customer={customer}/>
              ))}
            </tbody>
          </table>
          
          </div>
      </>
    )
  }
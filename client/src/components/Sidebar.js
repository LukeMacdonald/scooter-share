import React from 'react'
import ScooterImg from '../assets/imgs/scooter.png'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'

const SidebarItem = ({label, href, children}) => {
    return(
        <a 
          className='w-full flex items-center justify-start px-5 py-3 text-md hover:bg-gray-300 border-l-4 border-transparent hover:border-primaryDark'
          href={href}>
            {children}
            <p className='px-8'>{label}</p>
        </a>
    )
}

export const Sidebar = () => {
  return (
    <div className='w-80 h-dvh bg-white min-h-dvh border-r-2 flex flex-col justify-start items-start gap-3'>
        <div className='w-full flex justify-between items-center px-3 pt-3'>
            <img src={ScooterImg} alt='Logo' className='w-14 h-14'/>
            <h1 className='text-2xl font-bold '><span className='text-primaryDark'>Scooter</span><span className='text-primary'>Share</span></h1>
        </div>
        
        <hr className='w-full'/>
        <SidebarItem label='Home' href='/customer'>
            <FontAwesomeIcon icon={icon({name: 'home'})} />
        </SidebarItem>
        <SidebarItem label='Profile' href='/customer/profile'>
            <FontAwesomeIcon icon={icon({name: 'user'})} />
        </SidebarItem>
        <SidebarItem label='Bookings' href='/customer/bookings'>
            <FontAwesomeIcon icon={icon({name: 'calendar'})} />
        </SidebarItem>
        <SidebarItem label='Logout' href='/'>
            <FontAwesomeIcon icon={icon({name: 'right-from-bracket'})} />
        </SidebarItem>
        
   
    </div>
  )
}

export const AdminSidebar = () => {
    return (
      <div className='w-80 h-dvh bg-white min-h-dvh border-r-2 flex flex-col justify-start items-start gap-3'>
          <div className='w-full flex justify-between items-center px-3 pt-3'>
              <img src={ScooterImg} alt='Logo' className='w-14 h-14'/>
              <h1 className='text-2xl font-bold '><span className='text-primaryDark'>Scooter</span><span className='text-primary'>Share</span></h1>
          </div>
          
          <hr className='w-full'/>
          <SidebarItem label='Home' href='/admin'>
              <FontAwesomeIcon icon={icon({name: 'home'})} />
          </SidebarItem>
          <SidebarItem label='Scooters' href='/admin/scooter/pending'>
            <FontAwesomeIcon icon={icon({name: 'motorcycle'})} />
          </SidebarItem>
          <SidebarItem label='Logout' href='/'>
            <FontAwesomeIcon icon={icon({name: 'right-from-bracket'})} />
          </SidebarItem>
  </div>
    )
}

export const EngineerSidebar = () => {
    return (
      <div className='w-80 h-dvh bg-white min-h-dvh border-r-2 flex flex-col justify-start items-start gap-3'>
          <div className='w-full flex justify-between items-center px-3 pt-3'>
              <img src={ScooterImg} alt='Logo' className='w-14 h-14'/>
              <h1 className='text-2xl font-bold '><span className='text-primaryDark'>Scooter</span><span className='text-primary'>Share</span></h1>
          </div>
          
          <hr className='w-full'/>
          <SidebarItem label='Home' href='/admin'>
              <FontAwesomeIcon icon={icon({name: 'home'})} />
          </SidebarItem>
          <SidebarItem label='Profile' href='/engineer/profile'>
            <FontAwesomeIcon icon={icon({name: 'user'})} />
          </SidebarItem>
          <SidebarItem label='Logout' href='/'>
            <FontAwesomeIcon icon={icon({name: 'right-from-bracket'})} />
          </SidebarItem>
  </div>
    )
}
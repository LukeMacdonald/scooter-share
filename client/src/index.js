import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import Signup from './pages/Signup';
import Bookings from './pages/customer/Bookings';
import RouteTo from './pages/customer/Route';
import Profile from './pages/customer/Profile';
import Booking from './pages/customer/Booking';
import Login from './pages/Login';

import { CustomerDashboard, CustomerLayout } from './pages/customer/Dashboard';
import { EngineerDashboard, EngineerLayout } from './pages/engineer/Dashboard';
import { AdminLayout, AdminDashboard } from './pages/admin/Dashboard';

import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";

import './index.css';
import EditProfile from './pages/admin/EditProfile';
import EditScooter from './pages/admin/EditScooter';
import AddScooter from './pages/admin/AddScooter';
import DamagedScooter from './pages/admin/DamagedScooter';
import { AuthProvider } from './context/AuthContext';



const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route index element={<Login />} />
      <Route path='signup' element={<Signup />} />
      <Route path='customer' element={<CustomerLayout />}>
        <Route index element={<CustomerDashboard />} />
        <Route path='bookings' element={<Bookings />} />
        <Route path='route/:scooterID' element={<RouteTo/>}/>
        <Route path='profile' element={<Profile/>}/>
        <Route path='booking/:scooterID' element={<Booking/>}/>
      </Route>
      <Route path='admin' element={< AdminLayout/>}>
        <Route index element={<AdminDashboard />} />
        <Route path='edit/customer/:userId' element={<EditProfile/>}/>
        <Route path='edit/scooter/:scooterId' element={<EditScooter/>}/>
        <Route path='add/scooter' element={<AddScooter/>}/>
        <Route path='scooter/pending' element={<DamagedScooter/>}/>
      </Route>
      <Route path='engineer' element={< EngineerLayout/>}>
        <Route index element={<EngineerDashboard />} />
      </Route>
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <RouterProvider router={router} />
    </LocalizationProvider>

    </AuthProvider>

  </React.StrictMode>
)

reportWebVitals();

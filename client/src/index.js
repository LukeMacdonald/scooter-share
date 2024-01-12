import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Login from './pages/Login';
import {CustomerDashboard, EngineerDashboard, AdminDashboard, CustomerLayout} from './pages/Dashboard';
import Signup from './pages/Signup';
import Bookings from './pages/customer/Bookings';
import RouteTo from './pages/customer/Route';
import Profile from './pages/customer/Profile';
import Booking from './pages/customer/Booking';

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
      <Route path='engineer' element={<EngineerDashboard />} />
      <Route path='admin' element={<AdminDashboard />} />
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

import React, { useState } from 'react'
import useCustomerData from '../../hooks/useCustomerData'
import { cancelBooking, sendReport } from '../../api/api';
import { ReportModal } from '../../components/Modal';

const ActiveBooking = ({booking}) =>{

  const [report, setReport] = useState("");

  const handleReport = async () => {
    
    const data = {booking_id: booking.id, scooter_id: booking.scooter_id, report: report}

    await sendReport(data);

    handleClose();

    window.location.reload();
  }

  const handleCancel = async (bookingID) =>{

    await cancelBooking(bookingID)

    window.location.reload();
  }

  const [open, setOpen] = useState(false);

  const handleOpen = () => {
      setOpen(true);

  };

  const handleClose = () => {
      setOpen(false);
  };

  return (
    <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
            <td className='px-6 py-4'>{booking.date}</td>
            <td className='px-6 py-4'>{convertTo12HourFormat(booking.start_time)}</td>
            <td className='px-6 py-4'>{booking.scooter_id}</td>
            <td className='px-6 py-4'>
              <div className={`flex items-center`}>
                <div className={`h-2.5 w-2.5 rounded-full ${getStatusColor(booking.status)} me-2`}></div> {booking.status}
              </div>
            </td>
            <td className='px-6 py-4'>
              <a className='text-blue-700 hover:underline font-semibold' href={`/customer/route/${booking.scooter_id}`}>Directions</a>
            </td>
            <td className='px-6 py-4'>
              <button className='text-red-700 hover:underline font-semibold' onClick={()=>handleCancel(booking.id)}>Cancel</button>
            </td>
            <td className='px-6 py-4'>
              <button className='text-orange-700 hover:underline font-semibold' onClick={handleOpen}>Report</button>
            </td>
            <ReportModal handleClose={handleClose} handleConfirm={handleReport} open={open} value={report} setValue={setReport} />
          </tr>

  )
}

const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500'; // Green color for 'active'
      case 'cancelled':
        return 'bg-red-500'; // Red color for 'cancelled'
      case 'completed':
        return 'bg-blue-500'; // Blue color for 'completed'
      default:
        return 'bg-gray-500'; // Default color (gray) for other statuses
    }
};

function convertTo12HourFormat(time24hr) {
    // Parse the input time string
    const [hours, minutes] = time24hr.split(':');
    const parsedDate = new Date(0, 0, 0, hours, minutes);
  
    // Format as 12-hour time
    const time12hr = parsedDate.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
  
    return time12hr;
}


const Bookings = () => {

  let {bookings} = useCustomerData();

  return (
    <>
    <div className='w-full p-10'>
  <h1 className='text-2xl pb-3'>Upcoming Bookings</h1>
  <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
      <tr>
        <th scope="col" className="px-6 py-3">Date</th>
        <th scope="col" className="px-6 py-3">Start Time</th>
        <th scope="col" className="px-6 py-3">Scooter ID</th>
        <th scope="col" className="px-6 py-3">Status</th>
        <th></th>
        <th></th>
        <th>

        </th>
      </tr>
    </thead>
    <tbody>
      {bookings.map((booking, index) => (
        booking.status === 'active' && (
          <ActiveBooking booking={booking}/>
        )
      ))}
    </tbody>
  </table>
</div>
    <div className='w-full p-10'>
        <h1 className='text-2xl pb-3'>Booking History</h1>
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" className="px-6 py-3">Date</th>
                <th scope="col" className="px-6 py-3">Start Time</th>
                <th scope="col" className="px-6 py-3">End Time</th>
                <th scope="col" className="px-6 py-3">Scooter</th>
                <th scope="col" className="px-6 py-3">Status</th>
      
              </tr>
            </thead>
            <tbody>
              {bookings.map((booking, index) => (
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td className='px-6 py-4'>{booking.date}</td>
                    <td className='px-6 py-4'>{convertTo12HourFormat(booking.start_time)}</td>
                    <td className='px-6 py-4'>{convertTo12HourFormat(booking.end_time)}</td>
                    <td className='px-6 py-4'>{booking.scooter_id}</td>
                    <td className='px-6 py-4'>
                        <div class="flex items-center">
                            <div className={`h-2.5 w-2.5 rounded-full ${getStatusColor(booking.status)} me-2`}></div> {booking.status}
                        </div>
                    </td>
                </tr>
              ))}
            </tbody>
          </table>
    </div>
    
    
    
    </>
    
  )
}

export default Bookings
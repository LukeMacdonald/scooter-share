import React, { useState } from 'react'
import useCustomerData from '../../hooks/useCustomerData'
import { cancelBooking, sendReport } from '../../api/api';
import { ReportModal } from '../../components/Modal';
import { getBookingColor, convertTo12HourFormat } from "../../components/utils/utils"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'

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
      <div className="bg-white space-y-4 p-4 rounded-lg shadow">
        <div className="flex items-center space-x-4 text-md font-semibold">
        <div>{booking.date} at {convertTo12HourFormat(booking.start_time)}</div>
        </div>
        <div className='flex items-center space-x-4'>
          <FontAwesomeIcon icon={icon({name: 'motorcycle'})}/>
          <p>#{booking.scooter_id}</p>
        </div>
        <div>                      
          <div class="flex items-center uppercase text-sm">
              <div className={`h-2.5 w-2.5 rounded-full ${getBookingColor(booking.status)} me-2`}></div> {booking.status}
          </div>
        </div>
        <div className="flex items-center space-x-10 text-lg">

          <div><a className='text-blue-700 hover:underline font-semibold' href={`/customer/route/${booking.scooter_id}`}><FontAwesomeIcon icon={icon({name: 'route'})} /></a></div>
          <div> <button className='text-red-700 hover:underline font-semibold' onClick={()=>handleCancel(booking.id)}><FontAwesomeIcon icon={icon({name: 'trash'})} /></button></div>
          <div> <button className='text-orange-700 hover:underline font-semibold' onClick={handleOpen}><FontAwesomeIcon icon={icon({name: 'flag'})} /></button></div>
        </div>
        <ReportModal handleClose={handleClose} handleConfirm={handleReport} open={open} value={report} setValue={setReport} />
      </div>
  )
}




const Bookings = () => {

  let {bookings} = useCustomerData();

  return (
    <>
    <div className='w-full p-10'>
  <h1 className='text-2xl pb-3'>Upcoming Bookings</h1>
  <div className="grid grid-cols-2 lg:grid-cols-1 gap-4 border overflow-y-auto max-h-[30rem] p-2">
  {bookings.map((booking, index) => (
        booking.status === 'active' && (
          <ActiveBooking booking={booking}/>
        )
      ))}

  </div>

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
                            <div className={`h-2.5 w-2.5 rounded-full ${getBookingColor(booking.status)} me-2`}></div> {booking.status}
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
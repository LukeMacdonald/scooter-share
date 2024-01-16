import React from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    pt: 2,
    px: 4,
    pb: 3,
};

export const TopUpModal  = ({handleConfirm, handleClose, open, setAmount, value}) => {
    return(
        <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="parent-modal-title"
        aria-describedby="parent-modal-description"
      >
        <Box sx={{ ...style, width: 400 }}>
            <h1 className='text-xl pb-5'>Top Up Account</h1>
            <input 
            type='number'
            min={0}
            value={value}
            onChange={(event) => setAmount(event.target.value)}
            className='w-full border rounded-md p-2'
            placeholder='Enter Amount'
            />
            <div className='w-full flex justify-evenly items-center pt-5'>
                <button onClick={handleConfirm} className='bg-green-700 py-2 w-1/2 mx-2 rounded-md text-light'>Confirm</button>
                <button onClick={handleClose}className='bg-red-700 py-2 w-1/2 mx-2 rounded-md text-light'>Cancel</button>
            </div>
        </Box>
      </Modal>
    )
}
  
  
export const ReportModal = ({ handleConfirm, handleClose, open, setValue, value }) => {
    return (
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="parent-modal-title"
        aria-describedby="parent-modal-description"
      >
        <Box sx={{ ...style, width: 400 }}>
          <h1 className='text-xl pb-5'>Report Scooter</h1>
          <textarea
            value={value}
            onChange={(event) => setValue(event.target.value)}
            className='w-full border rounded-md p-2'
            placeholder='Enter Report'
            rows={4} // Set the number of visible rows
          />
          <div className='w-full flex justify-evenly items-center pt-5'>
            <button onClick={handleConfirm} className='bg-green-700 py-2 w-1/2 mx-2 rounded-md text-light'>Confirm</button>
            <button onClick={handleClose} className='bg-red-700 py-2 w-1/2 mx-2 rounded-md text-light'>Cancel</button>
          </div>
        </Box>
      </Modal>
    );
};

export const ViewReportModal = ({ handleClose, open, value }) => {
    return (
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="parent-modal-title"
        aria-describedby="parent-modal-description"
      >
        <Box sx={{ ...style, width: 600 }}>
          <h1 className='text-xl'>Maintenance Report</h1>
          <hr/>
          <p className='pt-5'>{value}</p>
          <div className='w-full flex justify-evenly items-center pt-5'>
            <button onClick={handleClose} className='bg-gray-500 py-2 w-1/2 mx-2 rounded-md text-light'>Close</button>
          </div>
        </Box>
      </Modal>
    );
};
import React, {useEffect, useState} from 'react'
import { topUp } from '../../api/api';
import useCustomerData from '../../hooks/useCustomerData';
import { TopUpModal } from '../../components/Modal';

const ProfileItem = ({value, label}) =>{
    return(
        <div className='w-1/2 mx-2'>
                <p className='font-bold'>{label}</p>
                <p className='w-full border p-2'>{value}</p>
        </div>
    )
}



const Profile = () => {

    const {user} = useCustomerData()

    const [open, setOpen] = useState(false);

    const [amount, setAmount] = useState(0);

    const handleOpen = () => {
        setOpen(true);

    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleTopUp = async (event) => {
        event.preventDefault();

        const userID = localStorage.getItem('user')

        const data = {
            user_id: userID,
            amount: amount
        }

        await topUp(data);

        setOpen(false)
        window.location.reload()
        
    }

    useEffect(()=>{
        setAmount(0);
    },[open])

  return (
    <>
      <div className='p-10 w-10/12 self-center flex flex-col gap-6'>
        <h1 className='uppercase text-xl'>User Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={user.username} label='Username'/>
            <ProfileItem value={user.role} label='Role'/>
        </div>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={user.first_name} label='First Name'/>
            <ProfileItem value={user.last_name} label='Last Name'/>
        </div>
        
        <h1 className='uppercase text-xl'>Contact Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={user.phone_number} label='Phone Number'/>
            <ProfileItem value={user.email} label='Email'/>
        </div>
        
        <h1 className='uppercase text-xl'>Payment Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'> 
            <div className='w-full mx-2'>
                <p className='font-bold'>Balance</p>
                <div className='w-full flex justify-start items-center'>
                    <p className='w-1/2 border p-2 mr-2'>$ {user.balance}</p>
                    <button onClick={handleOpen} className='self-center bg-dark p-2  text-light w-1/3 rounded-lg ml-2'>Top Up</button>
                </div>
            </div>
        </div>

      </div>
      <TopUpModal 
        handleClose={handleClose} handleConfirm ={handleTopUp} 
        value={amount} open={open} setAmount={setAmount}
       />
    </>

  )
}

export default Profile
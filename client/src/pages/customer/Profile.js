import React from 'react'

const ProfileItem = ({value, label}) =>{
    return(
        <div className='w-1/2 mx-2'>
                <p className='font-bold'>{label}</p>
                <p className='w-full border p-2'>{value}</p>
        </div>
    )
    

}

const Profile = () => {

    const userInfo = JSON.parse(localStorage.getItem("userInfo"))
    console.log(userInfo)
  return (
    <>
      <div className='p-10 w-10/12 self-center flex flex-col gap-6'>
        <h1 className='uppercase text-xl'>User Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={userInfo.username} label='Username'/>
            <ProfileItem value={userInfo.role} label='Role'/>
        </div>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={userInfo.first_name} label='First Name'/>
            <ProfileItem value={userInfo.last_name} label='Last Name'/>
        </div>
        
        <h1 className='uppercase text-xl'>Contact Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'>
            <ProfileItem value={userInfo.phone_number} label='Phone Number'/>
            <ProfileItem value={userInfo.email} label='Email'/>
        </div>
        
        <h1 className='uppercase text-xl'>Payment Information</h1>
        <hr className='w-full'/>
        <div className='w-full flex justify-between items-start'> 
            <div className='w-full mx-2'>
                <p className='font-bold'>Balance</p>
                <div className='w-full flex justify-start items-center'>
                    <p className='w-1/2 border p-2 mr-2'>$ {userInfo.balance}</p>
                    <button className='self-center bg-dark p-2  text-light w-1/3 rounded-lg ml-2'>Top Up</button>
                </div>
            </div>
        </div>

      </div>
    
        
    </>

  )
}

export default Profile
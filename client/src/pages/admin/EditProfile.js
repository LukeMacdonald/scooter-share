import React, { useEffect, useState } from 'react';
import { getCustomer, updateCustomer } from '../../api/api'; // Assuming you have an updateCustomer function
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const ProfileItem = ({ value, label, onChange, name, disabled }) => {
  return (
    <div className='w-1/2 mx-2'>
      <label className='font-bold'>{label}</label>
      <input
        type='text'
        className='w-full border p-2'
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(name, e.target.value)}
      />
    </div>
  );
};

const EditProfile = () => {
  const [user, setUser] = useState({});
  const { userId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getCustomer(userId);
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    };

    fetchUser();
  }, [userId]);

  const handleInputChange = (label, value) => {
    setUser((prevUser) => ({
      ...prevUser,
      [label.toLowerCase()]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(user);

    try {
      // Assuming you have an updateCustomer function
      await updateCustomer(user);


      console.log('User updated successfully!');
      navigate("/admin")
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className='p-10 w-10/12 self-center flex flex-col gap-6'>
        <h1 className='uppercase text-xl'>User Information</h1>
        <hr className='w-full' />
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={user.username}
            label='Username'
            onChange={handleInputChange}
            name='username'
            disabled={true}
          />
          <ProfileItem value={user.role} label='Role' onChange={handleInputChange} name='role' disabled={true} />
        </div>
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={user.first_name}
            label='First Name'
            onChange={handleInputChange}
            name='first_name'
            disabled={false}
          />
          <ProfileItem
            value={user.last_name}
            label='Last Name'
            onChange={handleInputChange}
            name='last_name'
            disabled={false}
          />
        </div>

        <h1 className='uppercase text-xl'>Contact Information</h1>
        <hr className='w-full' />
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={user.phone_number}
            label='Phone Number'
            onChange={handleInputChange}
            name='phone_number'
            disabled={false}
          />
          <ProfileItem value={user.email} label='Email' onChange={handleInputChange} name='email' disabled={true}/>
        </div>

        <div className='w-full flex items-center justify-center'>
            <button type='submit' className='mt-10 mx-5 bg-blue-500 text-white p-2 w-1/2 rounded-lg'>
                Save Changes
            </button>
            <a href='/admin' className='mt-10 mx-5 bg-gray-500 text-white p-2 w-1/2 rounded-lg text-center'>
                Cancel
            </a>
        </div>
      </div>
    </form>
  );
};

export default EditProfile;

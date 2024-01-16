import React, { useEffect, useState } from 'react';
import { saveScooter } from '../../api/api';
import { useNavigate } from 'react-router-dom';
import useGeolocation from '../../hooks/useGeolocation';

const ProfileItem = ({ value, label, onChange, name, disabled, isNumber }) => {
  return (
    <div className='w-1/3 mx-2'>
      <label className='font-bold'>{label}</label>
      <input
        type={isNumber ? 'number' : 'text'}
        className='w-full border p-2'
        value={value}
        readOnly={disabled}
        onChange={(e) => onChange(name, isNumber ? parseFloat(e.target.value) : e.target.value)}
        step={isNumber ? 'any' : undefined}
      />
    </div>
  );
};

const AddScooter = () => {
    const { center } = useGeolocation();
    const [scooter, setScooter] = useState({
      make: "",
      colour: "",
      cost: 0.0,
      longitude: 0.0,
      latitude: 0.0
    });
  
    useEffect(() => {
      if (center !== null && center !== undefined) {
        setScooter((prevScooter) => ({
          ...prevScooter,
          latitude: center.lat,
          longitude: center.lng
        }));
      }
    }, [center]);


  const navigate = useNavigate();

  

  console.log(center);

  const handleInputChange = (name, value) => {
    setScooter((prevScooter) => ({
      ...prevScooter,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      console.log(scooter);
      // Assuming you have an updateScooter function
      await saveScooter(scooter);
      
      console.log('Scooter updated successfully!');
      navigate("/admin")
    } catch (error) {
      console.error('Error updating scooter:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className='p-10 w-10/12 self-center flex flex-col gap-4'>
        <h1 className='uppercase text-xl'>Scooter Information</h1>
        <p className='text-sm'>Note: Scooter Location is Retrieved From Admins Current Location</p>
        <hr className='w-full' />
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={scooter.make}
            label='Make'
            onChange={handleInputChange}
            name='make'
            disabled={false}
          />
          <ProfileItem
            value={scooter.colour}
            label='Colour'
            onChange={handleInputChange}
            name='colour'
            disabled={false}
          />
          <ProfileItem
            value={scooter.cost}
            label='Cost (Per Hour)'
            onChange={handleInputChange}
            name='cost'
            disabled={false}
            isNumber
          />
          </div>
      
          
          <div className='w-full flex justify-between items-start mt-5'>
          <ProfileItem
            value={scooter.longitude}
            label='Longitude'
            onChange={handleInputChange}
            name='longitude'
            disabled={true}
          />
          <ProfileItem
            value={scooter.latitude}
            label='Latitude'
            onChange={handleInputChange}
            name='latitude'
            disabled={true}
            isNumber
          />
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

export default AddScooter;
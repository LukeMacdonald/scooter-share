import React, { useEffect, useState } from 'react';
import { getScooter, updateScooter } from '../../api/api';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const ProfileItem = ({ value, label, onChange, name, disabled, isNumber }) => {
  return (
    <div className='w-1/2 mx-2'>
      <label className='font-bold'>{label}</label>
      <input
        type={isNumber ? 'number' : 'text'}
        className='w-full border p-2'
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(name, isNumber ? parseFloat(e.target.value) : e.target.value)}
        step={isNumber ? 'any' : undefined}
      />
    </div>
  );
};

const EditScooter = () => {
  const [scooter, setScooter] = useState({});
  const { scooterId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchScooter = async () => {
      try {
        const scooterData = await getScooter(scooterId);
        console.log(scooterData);
        setScooter(scooterData);
      } catch (error) {
        console.error('Error fetching scooter:', error);
      }
    };

    fetchScooter();
  }, [scooterId]);

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
      await updateScooter(scooter);
      
      console.log('Scooter updated successfully!');
      navigate("/admin")
    } catch (error) {
      console.error('Error updating scooter:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className='p-10 w-10/12 self-center flex flex-col gap-6'>
        <h1 className='uppercase text-xl'>Scooter Information</h1>
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
        </div>
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={scooter.remaining_power}
            label='Remaining Power'
            onChange={handleInputChange}
            name='remaining_power'
            disabled={false}
            isNumber
          />
          <ProfileItem
            value={scooter.cost_per_time}
            label='Cost (Per Hour)'
            onChange={handleInputChange}
            name='cost_per_time'
            disabled={false}
            isNumber
          />
        </div>
        <div className='w-full flex justify-between items-start'>
          <ProfileItem
            value={scooter.status}
            label='Status'
            onChange={handleInputChange}
            name='status'
            disabled
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

export default EditScooter;

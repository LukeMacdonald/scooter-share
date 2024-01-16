import React, {useState, useEffect} from 'react'
import { useNavigate, useParams } from 'react-router-dom';
import { Input, initTE } from 'tw-elements';
import { makeBooking, scooterData } from '../../api/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro'
import { TimePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';

const maxHour = () => {
  // Get the current date and time
  const currentDate = dayjs();

  // Round up the current hour to the nearest integer
  const roundedHour = Math.ceil(currentDate.hour());

  // Calculate the wrapped hour (adding 2 and wrapping around if needed)
  const wrappedHour = (roundedHour + 2) % 24;

  // Set the wrapped hour and start of the hour using dayjs
  return currentDate.set('hour', wrappedHour).startOf('hour');
};

const Booking = () => {
  
  const { scooterID } = useParams();

  const [estimate, setEstimate] = useState(0)

  const [scooter, setScooter] = useState({});

  const [time, setTime] = useState(null)

  const [duration, setDuration] = useState(0)

  const navigate = useNavigate();

  const max = maxHour()

  const handleClick = async (event)=> {
    
    event.preventDefault()

    const userID = localStorage.getItem('user')
    
    const data = {
      user_id: userID,
      scooter_id: scooterID,
      start_time: `${time.$H.toString()}:${time.$m.toString()}`,
      duration: duration
    }

    await makeBooking(data)


    navigate("/customer")
  }
  
  useEffect(() => {
    const fetchScooter = async () => {
      try {
        const scooter = await scooterData(scooterID);
        setScooter(scooter);
      } catch (error) {
        console.error("Error fetching scooter data:", error);
      }
    };
    fetchScooter();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  useEffect(() => {
    initTE({ Input });
  } );

  const handleDuration = (num) => {
    if (duration + num >= 0 && duration + num <= 180){
      setDuration(duration + num);
    }
  }

  useEffect(() => {
    setEstimate(Number((scooter.cost_per_time * (duration / 60)).toFixed(2)));
  }, [duration, scooter.cost_per_time]);

  

  return (
    <div className='w-full h-full flex items-start justify-start'>
      <div className='w-2/3 h-full flex flex-col items-start justify-start pl-16'>
        <h1 className='text-3xl mt-10 font-bold font-montserrat'>Make a Booking</h1>
        <p className='font-semibold font-mono pt-8 text-lg'>Scooter Information</p>
        <p className='text-base pt-1'>Scooter ID: <span>{`${scooterID}`}</span></p>
        <p className='text-base py-2'> Description: <span>{`${scooter.make} (${scooter.colour})`}</span></p>
        <p className='text-base'>Cost: {`$ ${scooter.cost_per_time}`}</p>

        <p className='font-semibold font-mono pt-5 text-lg'>Booking Details</p>

        <p className='font-semibold font-mono text-base pt-3'>Start Time</p>
        <div className='mt-5 w-2/3'>
          <TimePicker
            label="Select Start Time"
            format="HH:mm"
            value={time}
            disablePast
            onChange={(newValue) => setTime(newValue)}
            maxTime={max}
            sx={{
              width: "100%", 
            }}
          />
          <p className='text-xs pt-3'>NOTE: Bookings can only be made 2 hours in advance</p>
          
        </div>
        <p className='font-semibold font-mono text-base mt-5 '>Duration (minutes)</p>
        <div className='w-full mt-5 flex items-center justify-start'>
        <div className="relative w-5/12" data-te-input-wrapper-init>
        <input
          type="number"
          min={0}
          max={180}
          name='duration'
          step={5}
          value={duration}
          readOnly  // Make the input read-only
          className="peer block min-h-[auto] w-full rounded border-0 bg-transparent px-3 py-4 leading-[1.6] text-md outline-none transition-all duration-200 ease-linear focus:placeholder:opacity-100 peer-focus:text-primary data-[te-input-state-active]:placeholder:opacity-100 motion-reduce:transition-none [&:not([data-te-input-placeholder-active])]:placeholder:opacity-0"
          id="duration"
        />
          <label
            htmlFor="duration"
            className="pointer-events-none absolute left-3 top-0 mb-0 max-w-[90%] origin-[0_0] truncate pt-[0.37rem] leading-[1.6] text-neutral-500 transition-all duration-200 ease-out peer-focus:-translate-y-[0.9rem] peer-focus:scale-[0.8] peer-focus:text-primary peer-data-[te-input-state-active]:-translate-y-[0.9rem] peer-data-[te-input-state-active]:scale-[0.8] motion-reduce:transition-none "
          >Select Duration</label>
         
        </div>
        <button className='bg-primary text-light p-3 w-1/12 mx-2 rounded-md' onClick={() => handleDuration(5)}><FontAwesomeIcon icon={icon({name: 'plus'})} /></button>
        <button className='bg-primary text-light p-3 w-1/12 mx-2 rounded-md' onClick={() => handleDuration(-5)}><FontAwesomeIcon icon={icon({name: 'minus'})} /></button>
        </div>
        <p className='text-xs pt-3'>NOTE: Max 2 hr bookings (180 minutes)</p>
        <div className='w-full flex justify-start items-center mt-8'>
          <button className='disabled:bg-primary/45 bg-primary p-2 rounded-md w-1/3  text-light' onClick={handleClick}>Book</button>
          <p className='text-sm pl-5'>Estimated Cost: ${`${estimate}`}</p>

      </div>
       
        
      </div>
     
    
      <div className='w-1/3 h-full bg-primary'></div>
    </div>
  );
}

export default Booking;

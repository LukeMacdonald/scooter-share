import React, { useState } from 'react'
import Layout from '../components/Layout'
import LandingGif from '../assets/imgs/landing.gif'
import { signup } from '../api/api'
import { useNavigate } from 'react-router-dom'
import { CustomAuthInput } from '../components/CustomInputs'

const Signup = () => {

    const [fields, setFields] = useState({
        email: "",
        password: "",
        firstName: "",
        lastName:"",
        role:"",
        phoneNumber:"",
        username:""
    });

    const [errorMessage, setErrorMessage] = useState("")

    const navigate = useNavigate();

    const handleChange = (event) => {
        event.preventDefault();
        const { name, value } = event.target;
        setFields((prevCredentials) => ({
            ...prevCredentials,
            [name]: value
        }));
    }
    const handleClick = async () => {
        try {
            const user = await signup(fields);
            navigate(`/${user.role}`);            
        } catch (error) {
            console.error('Login failed:', error);
            setErrorMessage(error.message);
        }
    };
    return (
        <main className='w-full h-screen max-h-screen'>
            <Layout>
                <div className='w-full h-full flex md:flex-col items-center justify-start'>
                <div className='w-7/12 md:w-full h-full flex flex-col items-center'>
                    <h1 className='text-3xl font-bold m-10 self-start'><span className='text-primaryDark'>Scooter</span><span className='text-primary'>Share</span></h1>
                    <div>
                        <img src={LandingGif} className='rounded-3xl p-5' alt='landing'/>
                    </div>
                </div>
                <div className='w-5/12 md:w-full h-full bg-primary flex flex-col justify-start items-center pt-24 gap-12 pb-10'>
                    <div className='text-center'>
                        <h1 className='text-4xl font-md text-light'>Welcome to ScooterShare</h1>
                        <h3 className='text-md font-md mt-2 text-light'>Create your Account</h3>
                    </div>
                    <div className='w-full flex flex-col justify-start items-center gap-10 px-20 '>
                        <div className='w-full flex justify-between items-center'>
                            <CustomAuthInput 
                              name='firstName'
                              label='First Name' 
                              value={fields.firstName} 
                              handleChange={handleChange} 
                              className='!w-1/2 mr-1'/>
                            <CustomAuthInput 
                              name='lastName' 
                              label='Last Name'
                              value={fields.lastName} 
                              handleChange={handleChange} 
                              className='!w-1/2 ml-1'/>
                        </div>
                        <CustomAuthInput name='username' label='Username' value={fields.username} handleChange={handleChange}/>
                        <CustomAuthInput name='email' label='Email' value={fields.email} handleChange={handleChange}/>
                        <CustomAuthInput name='phoneNumber' label='Phone Number' value={fields.phoneNumber} handleChange={handleChange}/>
                        <CustomAuthInput name='password' label='Password' value={fields.password} handleChange={handleChange}/>
            
                        <select 
                          name='role' 
                          className='w-full p-2 rounded-md' 
                          onChange={handleChange} 
                          value={fields.role}
                          >
                            <option value=''>Select Role</option>
                            <option value='customer'>Customer</option>
                            <option value='engineer'>Engineer</option>
                        </select>

                        {errorMessage && <p className='text-light font-semibold bg-red-500/70 p-2 px-5 rounded-lg w-2/3 text-center'>{errorMessage}</p>}
                    </div>
                    
                    <div className='w-2/3'>
                        <button 
                          className='w-full rounded-full py-3 bg-primaryDark text-light'
                          onClick={handleClick}
                        >
                            Login
                        </button>
                    </div>
                </div>
                </div>
            </Layout>
        </main> 
    )
}

export default Signup
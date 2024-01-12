import React, { useState } from 'react'
import Layout from '../components/Layout'
import LandingGif from '../assets/imgs/landing.gif'
import { login } from '../api/api'
import { useNavigate } from 'react-router-dom'

const Login = () => {

    const [credentials, setCredentials] = useState({
        email: "",
        password: ""
    });

    const [errorMessage, setErrorMessage] = useState("")

    const navigate = useNavigate();

    const handleChange = (event) => {
        event.preventDefault();
        const { name, value } = event.target;
        setCredentials((prevCredentials) => ({
            ...prevCredentials,
            [name]: value
        }));
    }
    const handleClick = async () => {
        try {
            const user = await login(credentials.email, credentials.password);
            console.log(user)
            localStorage.setItem('user', user.id)
            localStorage.setItem('userInfo', JSON.stringify(user))
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
                <div className='w-5/12 md:w-full h-full bg-primary flex flex-col justify-start items-center pt-24 gap-24 pb-10'>
                    <div className='text-center'>
                        <h1 className='text-4xl font-md text-light'>Welcome Back</h1>
                        <h3 className='text-md font-md mt-2 text-light'>Signin to your Account</h3>
                    </div>
                    <div className='w-2/3 flex flex-col justify-start items-center gap-10 '>
                        <input 
                          type='text' 
                          name='email'
                          placeholder='Enter Email' 
                          className='w-full p-2 rounded-md' 
                          onChange={handleChange} 
                          value={credentials.email}
                        />
                        <input 
                          type='text'
                          name='password' 
                          placeholder='Enter Password' 
                          className='w-full p-2 rounded-md' 
                          onChange={handleChange} 
                          value={credentials.password}
                        />
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

export default Login
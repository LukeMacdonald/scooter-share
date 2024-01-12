import axios from 'axios'


export function login(email, password) {
    return axios.post('http://localhost:5002/auth/login', { email, password })
        .then(response => response.data.user)
        .catch(error => {
            if (error.response.data.error){
                throw Error(error.response.data.error)
            }
            else{
                throw error
            }
        });
}

export function signup(fields) {
    return axios.post('http://localhost:5002/auth/signup', fields)
        .then(response => response.data.user)
        .catch(error => {
            if (error.response.data.error){
                throw Error(error.response.data.error)
            }
            else{
                throw error
            }
        });
}

export function customerData(){
    const userID = localStorage.getItem('user')
    return axios.get(`http://localhost:5002/customer/data/${userID}`)
        .then(response => response.data)
        .catch(error => {
            if (error.response.data.error){
                throw Error(error.response.data.error)
            }
            else{
                throw error
            }
        });
}

export function scooterData(scooterID){
    return axios.get(`http://localhost:5002/customer/scooter/${scooterID}`)
        .then(response => response.data)
        .catch(error => {
            if (error.response.data.error){
                throw Error(error.response.data.error)
            }
            else{
                throw error
            }
        });
}
import axios from 'axios'


export async function login(email, password) {
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

export async function signup(fields) {
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

/* Customer Routes */

export async function customerData(){
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

export async function scooterData(scooterID){
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

export async function makeBooking(data){
    return axios.post('http://localhost:5002/customer/book', data)
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

export async function cancelBooking(bookingID){
    return axios.delete(`http://localhost:5002/customer/cancel-booking/${bookingID}`)
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

export async function topUp(data){
    return axios.post('http://localhost:5002/customer/top-up-balance', data)
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

export async function sendReport(data){
    return axios.post('http://localhost:5002/customer/report', data)
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

/* Engineer Routes */


export async function engineerData(){
    return axios.get(`http://localhost:5002/engineer/scooters`)
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

export async function reportRepair(data){
    return axios.post('http://localhost:5002/engineer/fixed', data)
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


export async function adminData(){
    return axios.get(`http://localhost:5000/admin/data`)
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

export async function deleteCustomer(id){
    return axios.get(`http://localhost:5000/admin/customer/delete/${id}`)
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

export async function getCustomer(id){
    return axios.get(`http://localhost:5000/admin/customer/get/${id}`)
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
export async function updateCustomer(data){
    return axios.put(`http://localhost:5000/admin/customer/update`, data)
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

export async function deleteScooter(id){
    return axios.get(`http://localhost:5000/admin/scooter/delete/${id}`)
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

export async function getScooter(id){
    return axios.get(`http://localhost:5000/admin/scooter/get/${id}`)
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
export async function updateScooter(data){
    return axios.put(`http://localhost:5000/admin/scooter/update`, data)
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
export async function saveScooter(data){
    return axios.post(`http://localhost:5000/admin/scooter/submit`, data)
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

export async function getReportedScooters(){
    return axios.get(`http://localhost:5000/admin/repairs`)
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

export async function markScooterRepair(data){
    return axios.post(`http://localhost:5000/admin/scooter/report`, data)
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





export async function qr(scooterID, method, userID) {
    console.log(method)
    console.log(scooterID)
    console.log(userID)
    return axios.get(`http://localhost:5002/customer/scooter/${method}/${scooterID}/${userID}`)
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
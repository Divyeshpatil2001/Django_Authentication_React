import axios from "axios";
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";
import { toast } from 'react-toastify';


const token = localStorage.getItem('access') ? JSON.parse(localStorage.getItem('access')) : ""
const refresh_token = localStorage.getItem('refresh') ? JSON.parse(localStorage.getItem('refresh')) : ""

const baseUrl = "http://localhost:8000/api/v1"
const axiosInstance = axios.create({
    baseURL:baseUrl,
    'Content-type':"application/json",
    headers: {Authorization: localStorage.getItem('access') ? `Bearer ${token}` : null}
})

axiosInstance.interceptors.request.use(async req => {
    if (token) {
        req.headers.Authorization = `Bearer ${token}`
        const user = jwtDecode(token);
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1
        console.log(isExpired)
        if (!isExpired) {
            return req;
        }
        else {
            try {
                const res = await axios.post(`${baseUrl}/auth/token/refresh/`,{refresh:refresh_token})
                console.log(res.data)
                console.log("settingup")
                localStorage.setItem('access',JSON.stringify(res.data.access))
                req.headers.Authorization = `Bearer ${res.data.access}`
                return req;
            }
            catch (error) {
                console.log(error.response?.data)
                try {
                    const res = await axios.post(`${baseUrl}/auth/logout/`,{"refresh_token":refresh_token})
                    console.log("logout done")
                    localStorage.removeItem('access')
                    localStorage.removeItem('refresh')
                    localStorage.removeItem('user')
                }
                catch (error) {
                    console.log(error.response)
                    localStorage.removeItem('access')
                    localStorage.removeItem('refresh')
                    localStorage.removeItem('user')
                }
                
            }
        }
        return req; 
    }
})

export default axiosInstance;
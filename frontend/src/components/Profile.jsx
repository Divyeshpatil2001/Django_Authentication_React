import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axiosInstance from '../utils/axiosinstance';
import axios from 'axios';
import { toast } from 'react-toastify';

const Profile = () => {
  const user = JSON.parse(localStorage.getItem("user"));
  const jwt_access = localStorage.getItem("access");

  const navigate = useNavigate();

  useEffect(() => {
    if (jwt_access === null && !user) {
      navigate('/login')
      toast.error("your creditanls expired please relogin!!")
    }
    getSomeData()
  },[user,jwt_access])

  const refresh = JSON.parse(localStorage.getItem('refresh'));

  const getSomeData = async () => {
    try {
      const resp = await axiosInstance.get("/auth/test-auth/")
      console.log(resp.data)
    }
    catch (error) {
      console.log("test auth",error?.response)
      if (error.response?.status == 401) {
        navigate("/login")
        toast.error("refresh token is expired can you login again")
      }
    }
  }

  const handleLogout = async () => {
    try {
      const res = await axiosInstance.post("/auth/logout/",{'refresh_token':refresh})
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
      navigate('/login')
      toast.success('logout successfull')
    }
    catch (error) {
      console.log(error.response.data)
      toast.error(error.response.data[0],"sm")
    }
  }

  return (
    <div className='container'>
      <h2>hi {user && user.name}</h2>
      <p>welcome to dashboard</p>
      <button className='logout-btn btn' onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Profile
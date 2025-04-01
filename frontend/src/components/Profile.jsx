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
    // getSomeData()
  },[jwt_access,user])

  const refresh = JSON.parse(localStorage.getItem('refresh'));

  const getSomeData = async () => {
    try {
      const resp = await axiosInstance.get("/auth/test-auth/")
      console.log(resp.data)
    }
    catch (error) {
      console.log("test auth",error?.response)
      if (error.response?.status == 401) {
        console.log("dj")
        navigate("/login")
        toast.error("refresh token is expired can you login again")
      }
    }
  }

  const handleLogout = async () => {
    try {
      console.log(refresh)
      const res = await axiosInstance.post("/auth/logout/",{'refresh_token':refresh})
      console.log("Fdf")
      toast.success("Logout successful");
    } 
    catch (error) {
      console.log(error)
      if (error.response?.status === 401) {
          // 401 = Unauthorized → likely means the refresh token is expired or invalid (blacklist user)
          toast.error("Session expired, please log in again.");
      } else {
          toast.error(error.response?.data?.detail || "Logout failed. Try again.");
      }
    } 
    finally {
      // Always clear stored tokens & navigate to login
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");
      navigate("/login");
    }
  };
  return (
    <div className='container'>
      <h2>hi {user && user.name}</h2>
      <p>welcome to dashboard</p>
      <button className='logout-btn btn' onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Profile
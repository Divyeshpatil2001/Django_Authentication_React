import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const Signup = () => {
  const [formdata,setFormData] = useState({
    email : "",
    first_name : "",
    last_name : "",
    password : "",
    password2 : ""
  })

  const handleSignInwithGoogle = async (response) => {
    console.log(response)
    const payload = response?.credential
    // const server_res = axios.post("")
  }

  useEffect(() => {
    /* global google*/
    google.accounts.id.initialize({
      client_id: import.meta.env.VITE_CLIENT_ID,
      callback: handleSignInwithGoogle
    })
    google.accounts.id.renderButton(
      document.getElementById("signInDiv"),
      {theme:"outline",size:"large",text:"continue_width",shape:"circle",width:"300"}
    )
  }, [])
  

  const navigate = useNavigate()
  const [error,setError] = useState("")

  const handleOnChange = (e) => {
    setFormData({...formdata, [e.target.name]:e.target.value})
  }

  const {email,first_name,last_name,password,password2} = formdata 

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !first_name || !last_name || !password || !password2) {
      setError("All fields are required");
      return;
    }
  
    try {
      console.log(formdata);
      
      const res = await axios.post("http://localhost:8000/api/v1/auth/register/", formdata);
      console.log(res);
      
      if (res.status === 201) {
        const response = res.data;
        console.log(response);
        toast.success(response.message);
        navigate('/otp/verify');
      }
    } catch (error) {
      console.error("Registration Error:", error.response?.data || error.message);
  
      if (error.response) {
        setError(error.response.data?.message || "Something went wrong. Please try again.");
      } else {
        setError("Network error. Please check your connection.");
      }
    }
  }
  

  return (
    <div className="form-container">
      <div className="wrapper">
        <h2>Create an Account</h2>
        <form onSubmit={handleSubmit}>
        <p style={{color:"red",padding: "1px"}}>{error ? error : ""}</p>
            <div className="form-group">
                <label htmlFor="">First Name</label>
                <input type="text" value={first_name} onChange={handleOnChange} name="first_name" placeholder="Enter first name" />
            </div>

            <div className="form-group">
                <label htmlFor="">Last Name</label>
                <input type="text" value={last_name}  onChange={handleOnChange} name="last_name" placeholder="Enter last name" />
            </div>

            <div className="form-group">
                <label htmlFor="">Email Address</label>
                <input type="email" value={email} onChange={handleOnChange} name="email" placeholder="Enter email" />
            </div>

            <div className="form-group">
                <label htmlFor="">Password</label>
                <input type="password" value={password} onChange={handleOnChange} name="password" placeholder="Enter password" />
            </div>

            <div className="form-group">
                <label htmlFor="">Confirm Password</label>
                <input type="password" value={password2} onChange={handleOnChange} name="password2" placeholder="Confirm password" />
            </div>

            <button type="submit" className="btn">Sign Up</button>
        </form>
        <h3 className="text-option">Or </h3>
        <div className='githubContainer'>
          <button>Sign up with Github</button>
        </div>
        <div className='googleContainer' id='signInDiv' />
        </div>
    </div>
  );
};

export default Signup;
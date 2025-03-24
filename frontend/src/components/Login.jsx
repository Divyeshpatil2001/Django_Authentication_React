import axios from 'axios'
import React, { useState } from 'react'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router-dom'

const Login = () => {
  const [logindata,setLoginData] = useState({
    email : "",
    password : ""
  })

  const navigate = useNavigate()
  const [error,setError] = useState("")
  const [isloading,setIsLoading] = useState(false)

  const handleOnChange = (e) => {
    setLoginData({...logindata,[e.target.name]:e.target.value})
  }
  
  const  {email,password} = logindata

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !password) {
      setError("email and password both are required")
      return;
    }
    setIsLoading(true)
    try {
      const res = await axios.post("http://localhost:8000/api/v1/auth/login/",logindata);
      const response = res.data;

      const user = {"email":response.email,"name":response.full_name}
      localStorage.setItem("user",JSON.stringify(user))
      localStorage.setItem("access",JSON.stringify(response.access_token))
      localStorage.setItem("refresh",JSON.stringify(response.refresh_token))

      navigate("/dashboard")
      toast.success("login successfully")
      }
    catch (error) {
      const errorMessage = error.response?.data?.message || "Login failed. Please try again."
      toast.error(errorMessage)
    }
    finally {
      setIsLoading(false); 
    }
  }

  return (
    <div className="form-container">
      <div className="wrapper">
        <h2>Login</h2>
        <p style={{color:"red",padding: "1px"}}>{error ? error : ""}</p>
        <p style={{color:"red",padding: "1px"}}>{isloading ? "load" : ""}</p>
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="">Email Address:</label>
                <input type="text" className="email-form" name="email" value={email} onChange={handleOnChange}/>
            </div>

            <div className="form-group">
                <label htmlFor="">Password</label>
                <input type="password" className="password" name="password" value={password} onChange={handleOnChange}/>
            </div>

            <input type="submit" value="login" className="submitButton btn" />
        </form>
      </div>
    </div>
  )
}

export default Login
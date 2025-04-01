import axios from 'axios'
import React,{useState} from 'react'
import { toast } from 'react-toastify'

const ForgotPassword = () => {
  const [email,setEmail] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (email) {
      try {
        const res = axios.post("http://localhost:8000/api/v1/auth/password-reset/",{'email':email})
        toast.success("password reset link sent in email! please check!!")
      } catch (error) {
        console.log(error)
        toast.error("error while resetting password")
      }
    }
  }

  return (
    <div>
      <h2>Enter your registered email address</h2>
      <div className="wrapper">
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="">Email Address:</label>
                <input type="text" className="email-form" name="email" value={email} onChange={(e) => {setEmail(e.target.value)}}/>
            </div>

            <input type="submit" value="Send" className="submitButton btn vbtn" />
        </form>
      </div>
    </div>
  )
}

export default ForgotPassword
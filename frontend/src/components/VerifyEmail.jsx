import axios from 'axios'
import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'

const VerifyEmail = () => {
  const [otp,setOtp] = useState("")
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (otp) {
      try {
        const response = await axios.post("http://localhost:8000/api/v1/auth/verify-email/",{'otp':otp});
        navigate('/login');
        toast.success(response.data.message);
      }
      catch (error) {
        console.log(error)
        const errorMessage = error.response?.data?.message || "Verification failed. Please try again.";
        toast.error(errorMessage);
      }
    }
    else {
      toast.warning("please provide otp")
    }
  }

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="">Enter your Otp code:</label>
          <input type="text" name="otp" className="email-form" value={otp} onChange={(e) => setOtp(e.target.value)}/>
        </div>
        <input type='submit' className='vbtn btn' value="Send" />
      </form>
    </div>
  )
}

export default VerifyEmail;
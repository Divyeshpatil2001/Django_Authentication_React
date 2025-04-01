import React,{useState} from 'react'
import { useNavigate,useParams } from 'react-router-dom'
import axiosInstance from '../utils/axiosinstance';
import { toast } from 'react-toastify';

const ResetPassword = () => {
  const navigate = useNavigate();
  const {uid,token} = useParams();
  const [newpassword,setNewPassword] = useState({
    password:'',
    confirm_password:''
  });
  const handleChange = (e) => {
    setNewPassword({...newpassword,[e.target.name]:e.target.value})
  }
  const data = {
    'password':newpassword.password,
    'confirm_password':newpassword.confirm_password,
    'uidb64':uid,
    'token':token
  }
  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log(data)
    try {
        const response = await axiosInstance.patch('/auth/set-new-password/',data);
        const result = response.data
        console.log(response)
        navigate('/login')
        toast.success("password change successfull")
    } catch (error) {
        console.log(error)
        toast.error(error.response.data.error[0])
    }
  }
  return (
    <div className="form-container">
          <div className="wrapper">
            <h2>Enter your new password</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="">New Password:</label>
                    <input type="password" className="email-form" name="password" value={newpassword.password} onChange={handleChange}/>
                </div>
    
                <div className="form-group">
                    <label htmlFor="">Password</label>
                    <input type="password" className="password" name="confirm_password" value={newpassword.confirm_password} onChange={handleChange}/>
                </div>
    
                <input type="submit" value="Submit" className="submitButton btn" />
            </form>
          </div>
        </div>
  )
}

export default ResetPassword
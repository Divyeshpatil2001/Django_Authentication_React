// import { useState } from 'react'
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom'
import "./App.css"
import {Signup,Login,VerifyEmail,Profile,ForgotPassword} from './components'
import { ToastContainer } from 'react-toastify'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
     <Router>
      <ToastContainer />
      <Routes>
        <Route path='/' element={<Signup/>} />
        <Route path='/login' element={<Login/>} />
        <Route path='/dashboard' element={<Profile/>} />
        <Route path='/otp/verify' element={<VerifyEmail/>} />
        <Route path='/forget_password' element={<ForgotPassword/>} />
      </Routes>
     </Router>
    </>
  )
}

export default App

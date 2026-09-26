import { Routes, Route } from "react-router-dom"

import Login from "../pages/Login"
import ForgotPassword from "../pages/ForgotPassword"
import Register from "../pages/Register"
import HRCopilot from "../pages/HRCopilot"
import Interview from "../pages/Interview"
import JobMatching from "../pages/JobMatching"
import JobDetails from "../pages/JobDetails"


function AppRoutes() {
  return (
    <Routes>

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="/forgot-password"
        element={<ForgotPassword />}
      />

      <Route
        path="/hr-copilot"
        element={<HRCopilot />}
      />

      <Route
        path="/interview/:candidateId"
        element={<Interview />} 
      />
      
      <Route
        path="/jobs"
        element={<JobMatching />}
      />

      <Route
        path="/jobs/:id"
        element={<JobDetails />}
      />

    </Routes>
  )
}

export default AppRoutes
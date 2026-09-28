import { Routes, Route, Navigate } from "react-router-dom"

import Login from "../pages/Login"
import ForgotPassword from "../pages/ForgotPassword"
import Register from "../pages/Register"
import HRCopilot from "../pages/HRCopilot"
import Interview from "../pages/Interview"
import JobMatching from "../pages/JobMatching"
import JobDetails from "../pages/JobDetails"
import Ranking from "../pages/Ranking"
import CandidateDashboard from "../pages/CandidateDashboard"
import CandidateProfile from "../pages/CandidateProfile"
import Settings from "../pages/Settings"
import AppShell from "../AppShell"

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

      <Route element={<AppShell />}>
        <Route path="/" element={<Navigate to="/hr-copilot" replace />} />
        <Route path="/hr-copilot" element={<HRCopilot />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/recruiter-dashboard" element={<Ranking />} />
        <Route path="/interview/:candidateId" element={<Interview />} />
        <Route path="/jobs" element={<JobMatching />} />
        <Route path="/jobs/:id" element={<JobDetails />} />
        <Route path="/candidate-dashboard" element={<CandidateDashboard />} />
        <Route path="/candidate-profile" element={<CandidateProfile />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
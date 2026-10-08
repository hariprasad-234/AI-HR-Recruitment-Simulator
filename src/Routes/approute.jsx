import { Routes, Route, Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../Hooks/useAuth";

import Login from "../pages/Login";
import ForgotPassword from "../pages/ForgotPassword";
import Register from "../pages/Register";
import HRCopilot from "../pages/HRCopilot";
import Interview from "../pages/Interview";
import JobMatching from "../pages/JobMatching";
import JobDetails from "../pages/JobDetails";
import Ranking from "../pages/Ranking";
import CandidateDashboard from "../pages/CandidateDashboard";
import CandidateProfile from "../pages/CandidateProfile";
import UploadResume from "../pages/UploadResume";
import Settings from "../pages/Settings";
import AppShell from "../AppShell";
import LandingPage from "../pages/LandingPage";

function ProtectedRoute() {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}

function RoleRoute({ allowed }) {
  const { user } = useAuth();

  return allowed.includes(user?.role) ? (
    <Outlet />
  ) : (
    <Navigate
      to={
        user?.role === "candidate"
          ? "/candidate-dashboard"
          : "/hr-copilot"
      }
      replace
    />
  );
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Register />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>

          {/* Common route */}
          <Route path="/settings" element={<Settings />} />

          {/* Recruiter Routes */}
          <Route element={<RoleRoute allowed={["recruiter"]} />}>
            <Route path="/hr-copilot" element={<HRCopilot />} />
            <Route path="/recruiter-dashboard" element={<Ranking />} />
          </Route>

          {/* Candidate Routes */}
          <Route element={<RoleRoute allowed={["candidate"]} />}>
            <Route
              path="/interview/:candidateId"
              element={<Interview />}
            />
            <Route path="/jobs" element={<JobMatching />} />
            <Route path="/jobs/:id" element={<JobDetails />} />
            <Route
              path="/candidate-dashboard"
              element={<CandidateDashboard />}
            />
            <Route
              path="/candidate-profile"
              element={<CandidateProfile />}
            />
            <Route
              path="/upload-resume"
              element={<UploadResume />}
            />
          </Route>

        </Route>
      </Route>
    </Routes>
  );
}

export default AppRoutes;
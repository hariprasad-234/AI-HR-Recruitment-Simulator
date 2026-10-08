import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "./Hooks/useAuth"
import NotificationBell from "./components/NotificationBell"

const navLinkClass = ({ isActive }) => `border-b-2 px-1 py-3 text-sm font-medium ${isActive ? "border-emerald-700 text-emerald-900" : "border-transparent text-slate-600 hover:text-slate-900"}`

export default function AppShell() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login", { replace: true })
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
          <NavLink to={user?.role === "candidate" ? "/candidate-dashboard" : "/hr-copilot"} className="shrink-0 text-base font-bold tracking-tight text-slate-950">
            AI-HR-Recruitment-Simulator
          </NavLink>
          <nav aria-label="Main navigation" className="flex min-w-0 items-center gap-4 overflow-x-auto">
            {user?.role === "recruiter" ? (
              <>
                <NavLink to="/hr-copilot" className={navLinkClass}>Copilot</NavLink>
                <NavLink to="/recruiter-dashboard" className={navLinkClass}>Candidates</NavLink>
              </>
            ) : (
              <>
                <NavLink to="/candidate-dashboard" className={navLinkClass}>Dashboard</NavLink>
                <NavLink to="/jobs" className={navLinkClass}>Jobs</NavLink>
                <NavLink to="/candidate-profile" className={navLinkClass}>Profile</NavLink>
              </>
            )}
            <NavLink to="/settings" className={navLinkClass}>Settings</NavLink>
          </nav>
          <div className="flex shrink-0 items-center gap-2">
            <NotificationBell />
            <span className="hidden max-w-32 truncate text-sm text-slate-600 sm:block">{user?.name || user?.email || "Recruiter"}</span>
            <button type="button" onClick={handleLogout} className="rounded-md px-2 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900">Log out</button>
          </div>
        </div>
      </header>
      <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6">
        <Outlet />
      </main>
    </div>
  )
}

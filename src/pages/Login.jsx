import { useState } from "react"
import { Link } from "react-router-dom"
import { loginUser } from "../Services/authServices"
import { useAuth } from "../Hooks/useAuth"

function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
  e.preventDefault()

  setError("")

  if (!email || !password) {
    setError("Please enter your email and password")
    return
  }

  if (!email.includes("@")) {
    setError("Please enter a valid email address")
    return
  }

  try {
    setLoading(true)

    const result = await loginUser(email, password)

    console.log("Login response:", result)

    // Backend will return the real response later.
    // For now, show an error because no backend is connected.
    if (!result) {
      setError("Invalid email or password")
      return
    }
    login(result.user, rememberMe)

  } catch (error) {
    setError("Unable to login. Please try again.")
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg">

        <h1 className="text-3xl font-bold text-center">
          Login
        </h1>

        <p className="mt-2 text-center text-gray-500">
          Login to your account
        </p>

        {/* ERROR MESSAGE */}
        {error && (
          <div className="mt-6 rounded-lg bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6">

          {/* EMAIL */}
          <label className="block text-sm font-medium text-gray-700">
            Email
          </label>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none"
          />

          {/* PASSWORD */}
          <label className="mt-4 block text-sm font-medium text-gray-700">
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none"
          />

          {/* REMEMBER + FORGOT */}
          <div className="mt-4 flex items-center justify-between">

            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4"
              />

              <span className="text-sm text-gray-600">
                Remember me
              </span>
            </label>

            <Link
              to="/forgot-password"
              className="text-sm font-medium text-blue-600 hover:text-blue-700"
            >
              Forgot Password?
            </Link>

          </div>

          {/* LOGIN BUTTON */}
          <button
        type="submit"
        disabled={loading}
        className="mt-6 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? "Logging in..." : "Login"}
      </button>

        </form>

        {/* SIGNUP */}
        <p className="mt-6 text-center text-sm text-gray-600">
          Don't have an account?{" "}
          <Link
            to="/signup"
            className="font-medium text-blue-600 hover:text-blue-700"
          >
            Sign Up
          </Link>
        </p>

      </div>
    </div>
  )
}

export default Login
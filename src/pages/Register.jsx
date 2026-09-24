import { useState } from "react"
import { Link } from "react-router-dom"

function Register() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [role, setRole] = useState("")
  const [error,seterror]=useState("")
  const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
{error && (
  <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">
    {error}
  </div>
)}
const getPasswordStrength = (password) => {

  if (password.length < 6) {
    return "weak"
  }

  if (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[0-9]/.test(password)
  ) {
    return "strong"
  }

  return "medium"
}


  const handleSubmit = (e) => {
  e.preventDefault()

  if (!name || !email || !password) {
    alert("Please fill all fields")
    return
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters")
    return
  }
  if(password!=confirmPassword){
    alert("Password does not match");
    return
  }
  if (!role) {
  alert("Please select a role")
  return
  
}
  console.log("Name:", name)
  console.log("Email:", email)
  console.log("Password:", password)
  console.log("Role:",role);
}
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">

        <h1 className="text-3xl font-bold text-center">
          Create Account
        </h1>

        <p className="text-gray-700 text-center mt-4">
          Join AI HR Recruitment
        </p>
        <p>
          <br>
          </br>
        </p>
        <form onSubmit={handleSubmit} className="mt-6">

  <div>
    <label className="block text-sm font-medium text-gray-700">
      Full Name
    </label>

    <input
  type="text"
  placeholder="Enter your full name"
  value={name}
  onChange={(e) => setName(e.target.value)}
  className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3"
/>
<p>
          <br>
          </br>
        </p>
  </div>
  <div className="mt-4">


  <label className="block text-sm font-medium text-gray-700">
    Email
  </label>

  <input
  type="email"
  placeholder="Enter your email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"

/>
<p>
          <br>
          </br>
        </p>

</div>
<div className="mt-4">

  <label className="block text-sm font-medium text-gray-700">
    Password
  </label>

  <input
  type="password"
  placeholder="Create a password"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"


/>
{password && (
  <p className="mt-2 text-sm">
    Password strength:{" "}
    <span className="font-semibold">
      {getPasswordStrength(password)}
    </span>
  </p>
)}
<p>
          <br>
          </br>
        </p>
<div className="mt-4">

  <label className="block text-sm font-medium text-gray-700">
    Confirm Password
  </label>

  <input
    type="password"
    placeholder="Confirm your password"
    value={confirmPassword}
    onChange={(e) => setConfirmPassword(e.target.value)}
    className="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100"

  />
  <p>
          <br>
          </br>
        </p>

</div>

</div>
<div className="mt-4">

  <div className="mt-2 flex gap-6">

    <label className="flex items-center gap-2">
      <input
  type="radio"
  name="role"
  value="candidate"
  checked={role === "candidate"}
  onChange={(e) => setRole(e.target.value)}
/>
      Candidate
    </label>

    <label className="flex items-center gap-2">
    <input
  type="radio"
  name="role"
  value="recruiter"
  checked={role === "recruiter"}
  onChange={(e) => setRole(e.target.value)}
/>
      Recruiter
    </label>

  </div>

</div>
<button
  type="submit"
  className="mt-6 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700"
>
  Create Account
</button>
<p className="mt-6 text-center text-sm text-gray-600">
  Already have an account?{" "}
  <Link
  to="/login"
  className="font-semibold text-blue-600 hover:text-blue-700"
>
  Login
</Link>
</p>

</form>
        
      </div>

    </div>
  )
}

export default Register
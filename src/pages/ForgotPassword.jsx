import { useState } from "react"

function ForgotPassword() {
  const [email, setEmail] = useState("")
  const [sent, setSent] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!email) {
      alert("Please enter your email")
      return
    }

    setSent(true)
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg">

        {!sent ? (
          <>
            <h1 className="text-3xl font-bold text-center">
              Forgot Password?
            </h1>

            <p className="mt-2 text-center text-gray-500">
              Enter your email and we'll send you a reset link.
            </p>

            <form onSubmit={handleSubmit} className="mt-6">

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

              <button
                type="submit"
                className="mt-6 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Send Reset Link
              </button>

            </form>
          </>
        ) : (
          <div className="text-center">

            <h1 className="text-3xl font-bold">
              Reset Link Sent
            </h1>

            <p className="mt-3 text-gray-600">
              If an account exists for {email}, a password reset link
              has been sent.
            </p>

          </div>
        )}

      </div>

    </div>
  )
}

export default ForgotPassword
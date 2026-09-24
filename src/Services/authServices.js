export async function loginUser(email, password) {
  console.log("Login request:", {
    email,
    password,
  })

  return null
}

export async function signupUser(userData) {
  console.log("Signup request:", userData)

  return null
}

export async function forgotPassword(email) {
  console.log("Forgot password request:", email)

  return null
}
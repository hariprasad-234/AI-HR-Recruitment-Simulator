import { apiRequest } from "./apiClient"

export function loginUser(email, password) {
  return apiRequest("/api/auth/login", {
    method: "POST",
    body: { email, password },
  })
}

export function signupUser(userData) {
  return apiRequest("/api/auth/register", {
    method: "POST",
    body: userData,
  })
}

export function forgotPassword(email) {
  return apiRequest("/api/auth/forgot-password", {
    method: "POST",
    body: { email },
  })
}
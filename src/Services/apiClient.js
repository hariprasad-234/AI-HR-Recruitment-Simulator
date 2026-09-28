const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "")

export async function apiRequest(path, { method = "GET", body, signal } = {}) {
  const token = localStorage.getItem("token")
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      Accept: "application/json",
      ...(body !== undefined && { "Content-Type": "application/json" }),
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    ...(body !== undefined && { body: JSON.stringify(body) }),
    signal,
  })

  if (!response.ok) {
    let message = `Request failed (${response.status}). Please try again.`
    try {
      const payload = await response.json()
      message = payload.detail || payload.message || message
    } catch {
      // Keep the status-based message when the server sends no JSON body.
    }
    throw new Error(message)
  }

  if (response.status === 204) return null
  const contentType = response.headers.get("content-type") || ""
  return contentType.includes("application/json") ? response.json() : null
}

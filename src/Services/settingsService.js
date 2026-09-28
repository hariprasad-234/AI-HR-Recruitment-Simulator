import { apiRequest } from "./apiClient"

export async function getNotifications() {
  const data = await apiRequest("/api/notifications")
  const notifications = Array.isArray(data) ? data : data?.notifications
  return Array.isArray(notifications) ? notifications : []
}

export function markNotificationRead(id) {
  return apiRequest(`/api/notifications/${encodeURIComponent(id)}/read`, { method: "PATCH" })
}

export async function getNotificationPreferences() {
  const data = await apiRequest("/api/settings")
  return data?.notification_preferences || data?.notifications || data || {}
}

export function updateNotificationPreferences(preferences) {
  return apiRequest("/api/settings/notifications", { method: "PATCH", body: preferences })
}

export function updatePassword(currentPassword, newPassword) {
  return apiRequest("/api/auth/change-password", {
    method: "POST",
    body: { current_password: currentPassword, new_password: newPassword },
  })
}

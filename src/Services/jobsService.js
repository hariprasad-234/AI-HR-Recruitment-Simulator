import { apiRequest } from './apiClient'

export function getJobs() {
  return apiRequest('/api/jobs')
}

export function getJobById(id) {
  return apiRequest(`/api/jobs/${encodeURIComponent(id)}`)
}

export function applyForJob(id) {
  return apiRequest(`/api/jobs/${encodeURIComponent(id)}/apply`, { method: 'POST' })
}

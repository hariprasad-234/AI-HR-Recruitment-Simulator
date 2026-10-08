import { apiRequest } from './apiClient'

export function getCandidateProfile() {
  return apiRequest('/api/candidate/profile')
}

export function getCandidateApplications() {
  return apiRequest('/api/candidate/applications')
}

export function updateCandidateProfile(updatedProfile) {
  return apiRequest('/api/candidate/profile', { method: 'PATCH', body: updatedProfile })
}

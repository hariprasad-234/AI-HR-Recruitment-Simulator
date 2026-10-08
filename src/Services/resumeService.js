const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

export function uploadResume(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `${API_BASE_URL}/api/resume/upload`)
    const token = localStorage.getItem('token') || sessionStorage.getItem('token')
    if (token) xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) onProgress(Math.round((event.loaded / event.total) * 100))
    }
    xhr.onload = () => {
      let payload = {}
      try { payload = JSON.parse(xhr.responseText || '{}') } catch {}
      if (xhr.status >= 200 && xhr.status < 300) resolve(payload)
      else reject(new Error(payload.detail || 'Resume upload failed.'))
    }
    xhr.onerror = () => reject(new Error('Network error during resume upload.'))
    const formData = new FormData()
    formData.append('resume', file)
    xhr.send(formData)
  })
}

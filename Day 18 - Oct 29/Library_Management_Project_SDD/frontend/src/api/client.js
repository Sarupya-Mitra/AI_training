import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api/v1',
  withCredentials: true, // send the HttpOnly session cookie
  headers: { 'Content-Type': 'application/json' },
})

export default client
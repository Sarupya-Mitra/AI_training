import { createContext, useContext, useEffect, useState } from 'react'
import client from '../api/client'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
const AuthContext = createContext(null)

// Mock sign-in: role comes from the e-mail domain (spec rule P02).
function mockLogin(email, password) {
  const e = email.trim().toLowerCase()
  const domain = e.split('@')[1]
  const role = domain === 'lib.sample.com' ? 'Librarian' : domain === 'bor.sample.com' ? 'Borrower' : null
  if (!role || !password) throw { response: { status: 401 } }
  return { id: `mock-${e}`, email: e, role, full_name: e.split('@')[0], must_change_password: false }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        if (USE_MOCK) {
          const saved = sessionStorage.getItem('mockUser')
          if (alive && saved) setUser(JSON.parse(saved))
        } else {
          const { data } = await client.get('/me')
          if (alive) setUser(data)
        }
      } catch {
        // no session: the visitor stays signed out
      } finally {
        if (alive) setLoading(false)
      }
    })()
    return () => { alive = false }
  }, [])

  async function login(email, password) {
    let u
    if (USE_MOCK) {
      u = mockLogin(email, password)
      sessionStorage.setItem('mockUser', JSON.stringify(u))
    } else {
      const { data } = await client.post('/auth/login', { email, password })
      u = data
    }
    setUser(u)
    return u
  }

  async function logout() {
    try {
      if (USE_MOCK) sessionStorage.removeItem('mockUser')
      else await client.post('/auth/logout')
    } finally {
      setUser(null)
    }
  }

  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
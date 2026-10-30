import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ roles, children }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) return <p>Loading…</p>
  if (!user) {
    const target = encodeURIComponent(location.pathname + location.search)
    return <Navigate to={`/login?redirect=${target}`} replace />
  }
  if (roles && !roles.includes(user.role)) {
    return <p role="alert">This page is unavailable for your account.</p>
  }
  return children
}
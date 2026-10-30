import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// Navigation per spec UI06
const LINKS = {
  Visitor: [['/books', 'All Books'], ['/login', 'Sign in']],
  Borrower: [['/books', 'All Books'], ['/my-loans', 'My Loans'], ['/my-profile', 'My Profile']],
  Librarian: [['/books', 'All Books'], ['/borrowers', 'Borrowers'], ['/inventory', 'Inventory'], ['/loans', 'All Loans']],
}

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const links = LINKS[user ? user.role : 'Visitor']

  async function handleLogout() {
    await logout()
    navigate('/books')
  }

  return (
    <header className="nav">
      <strong className="brand">Library</strong>
      <nav aria-label="Main">
        {links.map(([to, label]) => (
          <NavLink key={to} to={to}>{label}</NavLink>
        ))}
      </nav>
      {user && (
        <div className="nav-user">
          <span>{user.full_name} ({user.role})</span>
          <button onClick={handleLogout}>Sign out</button>
        </div>
      )}
    </header>
  )
}
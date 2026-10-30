import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import AllBooks from '../pages/AllBooks'
import BookDetails from '../pages/BookDetails'
import SignIn from '../pages/SignIn'

const Placeholder = ({ name }) => <h2>{name} (coming in a later step)</h2>
const guard = (roles, name) => (
  <ProtectedRoute roles={roles}><Placeholder name={name} /></ProtectedRoute>
)

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/books" replace />} />
      <Route path="/books" element={<AllBooks />} />
      <Route path="/books/:id" element={<BookDetails />} />
      <Route path="/login" element={<SignIn />} />

      <Route path="/my-profile" element={guard(['Borrower'], 'My Profile')} />
      <Route path="/my-loans" element={guard(['Borrower'], 'My Loans')} />

      <Route path="/borrowers" element={guard(['Librarian'], 'Borrowers')} />
      <Route path="/borrowers/new" element={guard(['Librarian'], 'Create Borrower')} />
      <Route path="/borrowers/:id" element={guard(['Librarian'], 'Borrower Details')} />
      <Route path="/inventory" element={guard(['Librarian'], 'Inventory')} />
      <Route path="/loans" element={guard(['Librarian'], 'All Loans')} />

      <Route path="*" element={<p>Not found or unavailable.</p>} />
    </Routes>
  )
}
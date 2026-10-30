import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getBook } from '../api/books'
import { useAuth } from '../context/AuthContext'

export default function BookDetails() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [book, setBook] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    getBook(id).then(setBook).catch((e) =>
      setError(e?.response?.status === 404 ? 'Not found or unavailable.' : 'Could not load this book.'))
  }, [id])

  function handleBorrow() {
    if (!user) {
      navigate(`/login?redirect=${encodeURIComponent(`/books/${id}`)}`)
      return
    }
    setMessage('Borrowing will be connected in step 4.') // placeholder
  }

  if (error) return <p role="alert" className="error">{error}</p>
  if (!book) return <p>Loading…</p>

  return (
    <section className="card">
      <p><Link to="/books">← All Books</Link></p>
      <h2>{book.title}</h2>
      <dl>
        <dt>Author</dt><dd>{book.author}</dd>
        <dt>ISBN</dt><dd>{book.isbn}</dd>
        <dt>Publisher</dt><dd>{book.publisher || '—'}</dd>
        <dt>Category</dt><dd>{book.category}</dd>
        <dt>Year</dt><dd>{book.publication_year}</dd>
        <dt>Availability</dt>
        <dd>{book.available_copies > 0 ? `Available (${book.available_copies} copies)` : 'Not available'}</dd>
      </dl>
      {user?.role !== 'Librarian' && (
        <button disabled={book.available_copies === 0} onClick={handleBorrow}>
          {book.available_copies === 0 ? 'Not available' : 'Borrow'}
        </button>
      )}
      {message && <p role="status">{message}</p>}
    </section>
  )
}
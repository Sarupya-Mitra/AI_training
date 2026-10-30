import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { listBooks } from '../api/books'
import { useAuth } from '../context/AuthContext'

const PAGE_SIZE = 20

export default function AllBooks() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [q, setQ] = useState('')
  const [category, setCategory] = useState('')
  const [available, setAvailable] = useState(false)
  const [page, setPage] = useState(1)
  const [data, setData] = useState({ items: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setError('')
    try {
      setData(await listBooks({ q, category, available, page, pageSize: PAGE_SIZE }))
    } catch {
      setError('Could not load books.')
    } finally {
      setLoading(false)
    }
  }, [q, category, available, page])

  useEffect(() => { setLoading(true); load() }, [load])

  // UI07: refresh every 30 s while the tab is active
  useEffect(() => {
    const id = setInterval(() => { if (!document.hidden) load() }, 30000)
    return () => clearInterval(id)
  }, [load])

  function handleBorrow(book) {
    // Visitors go to sign in; the book page is the return target (rule P05)
    if (!user) navigate(`/login?redirect=${encodeURIComponent(`/books/${book.id}`)}`)
    else navigate(`/books/${book.id}`)
  }

  const clearFilters = () => { setQ(''); setCategory(''); setAvailable(false); setPage(1) }
  const lastPage = Math.max(1, Math.ceil(data.total / PAGE_SIZE))

  return (
    <section>
      <h2>All Books</h2>
      <div className="filters">
        <div>
          <label htmlFor="q">Search</label>
          <input id="q" value={q} maxLength={100} placeholder="Title, author or ISBN"
            onChange={(e) => { setQ(e.target.value); setPage(1) }} />
        </div>
        <div>
          <label htmlFor="cat">Category</label>
          <input id="cat" value={category} placeholder="e.g. Fiction"
            onChange={(e) => { setCategory(e.target.value); setPage(1) }} />
        </div>
        <label className="check">
          <input type="checkbox" checked={available}
            onChange={(e) => { setAvailable(e.target.checked); setPage(1) }} /> Available only
        </label>
        <button onClick={load}>Refresh</button>
      </div>

      {loading && <p>Loading…</p>}
      {error && <p role="alert" className="error">{error} <button onClick={load}>Retry</button></p>}

      {!loading && !error && data.items.length === 0 && (
        <p>No books found. <button onClick={clearFilters}>Clear filters</button></p>
      )}

      {data.items.length > 0 && (
        <table>
          <thead>
            <tr><th>Title</th><th>Author</th><th>Category</th><th>Availability</th><th></th></tr>
          </thead>
          <tbody>
            {data.items.map((b) => (
              <tr key={b.id}>
                <td><Link to={`/books/${b.id}`}>{b.title}</Link></td>
                <td>{b.author}</td>
                <td>{b.category}</td>
                <td>{b.available_copies > 0 ? `Available (${b.available_copies})` : 'Not available'}</td>
                <td>
                  {user?.role !== 'Librarian' && (
                    <button disabled={b.available_copies === 0} onClick={() => handleBorrow(b)}>Borrow</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="pager">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</button>
        <span>Page {page} of {lastPage} ({data.total} books)</span>
        <button disabled={page >= lastPage} onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </section>
  )
}
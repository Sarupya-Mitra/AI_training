import client from './client'
import { MOCK_BOOKS } from './mockData'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export async function listBooks({ q = '', category = '', available = false, page = 1, pageSize = 20 } = {}) {
  if (USE_MOCK) {
    const needle = q.trim().toLowerCase()
    const cat = category.trim().toLowerCase()
    const items = MOCK_BOOKS
      .filter((b) => !needle || [b.title, b.author, b.isbn].some((v) => v.toLowerCase().includes(needle)))
      .filter((b) => !cat || b.category.toLowerCase() === cat)
      .filter((b) => !available || b.available_copies > 0)
      .sort((a, b) => a.title.localeCompare(b.title))
    const start = (page - 1) * pageSize
    return { items: items.slice(start, start + pageSize), page, page_size: pageSize, total: items.length }
  }
  const params = { page, page_size: pageSize }
  if (q.trim()) params.q = q.trim()
  if (category.trim()) params.category = category.trim()
  if (available) params.available = true
  const { data } = await client.get('/books', { params })
  return data
}

export async function getBook(id) {
  if (USE_MOCK) {
    const book = MOCK_BOOKS.find((b) => b.id === id)
    if (!book) throw { response: { status: 404 } }
    return book
  }
  const { data } = await client.get(`/books/${id}`)
  return data
}
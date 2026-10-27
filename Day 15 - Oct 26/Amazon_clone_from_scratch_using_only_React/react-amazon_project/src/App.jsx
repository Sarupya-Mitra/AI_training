import { useState } from 'react'
import './App.css'
import { BrowserRouter, Link, Route,Routes } from 'react-router-dom'
import Home from './pages/Home'
import DisplayProduct from './pages/DisplayProduct'
import Login from './pages/Login'
import { AuthProvider } from './context/AuthProvider'
import DisplayCart from './pages/DisplayCart'
import ProtectedRoute from './components/ProtectedRoute'
import Payment from './pages/Payment'
import Logout from './pages/Logout'

function App() {
  const [products,setProducts] = useState(
    [{id : 1,name : "Wireless Mouse", price : 1200},
      {id : 2,name : "Monitor" , price : 20000},
      {id : 3, name : "Portable Speakers" , price : 6000}
  ])
  return(
    <AuthProvider>
    <BrowserRouter>
      <nav>
        <Link to="/login">Login</Link>
        {" | "}
        <Link to="/cart">Cart</Link>
        {" | "}
        <Link to="/logout">Logout</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home products={products}/>}/>
        <Route path="/products/:id" element={<DisplayProduct products={products}/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/cart" element={<DisplayCart/>}/>
        <Route path="/logout" element={<Logout />}/>
        <Route element={<ProtectedRoute/>}>
          <Route path="/payment" element={<Payment/>}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
    </AuthProvider>
  )
}

export default App

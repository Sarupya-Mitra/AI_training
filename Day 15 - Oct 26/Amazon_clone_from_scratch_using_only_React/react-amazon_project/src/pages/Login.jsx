import { useState } from "react"
import { useAuth } from "../context/AuthProvider"
import { useLocation, useNavigate } from "react-router-dom"
export default function Login(){
    const {login} = useAuth()
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    const [error,setError] = useState("")
    const navigate = useNavigate()

    const location = useLocation()

    function handleSubmit(event){
        event.preventDefault()

        const success = login(email,password)
        if (success){
            const destination = location.state?.from?.pathname || "/"
            navigate(destination,{replace:true})
        }
        else{
            setError("Invalid Email or Password")
        }
    }

    return (
        <div className="container">
            <h1>Login:</h1>
            <form onSubmit={handleSubmit}>
                <input type="email" placeholder="Email" value={email} 
                onChange={(e) => setEmail(e.target.value)} required/>

                <input type="text" placeholder="Password" value={password} 
                onChange={(e) => setPassword(e.target.value)} required/>
                <button type="submit">Submit</button>
            </form>
            {error && <p className="error">{error}</p>}
            <p>Demo email: admin@example.com</p>
            <p>Demo password: 1234</p>
        </div>
    )


}
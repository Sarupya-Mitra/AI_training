import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./context/AuthProvider";
import { useState } from "react";

export default function Login(){
    const {login} = useAuth()
    const location = useLocation()
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    const navigate = useNavigate()
    const [error,setError] = useState("")

    function handlelogin(event)
    {
        event.preventDefault()
        const success = login(email,password)
        if(success){
            const path = location.state?.from?.pathname || "/";
            navigate(path)
        }
        else{ setError("Invalid email or password")}
    }
  
    return(
        <div>
            <form onSubmit={handlelogin}>
                <input type="text" value={email} onChange={(e)=>(setEmail(e.target.value))} 
                placeholder="Enter email"/>

                <input type="text" value={password} onChange={(e)=>setPassword(e.target.value)}
                placeholder="Enter Password" />
                {error && <p>{error}</p>}  
                {/* //If error is present then this <p></p> tag will be shown */}
                <button type="submit">Login</button>
            </form>

        </div>
    );
}
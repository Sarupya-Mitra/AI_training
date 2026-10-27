import { useAuth } from "../context/AuthProvider"
import { useNavigate } from "react-router-dom"
export default function Logout(){
    const navigate = useNavigate()
    const {logout} = useAuth()
    function handlelogout(){
        logout()
        navigate("/")
    }
    return(
        <div>
            <h3> Are you sure you want to logout?</h3>
            <button onClick={handlelogout}>Log Out</button>
            <button onClick={()=> navigate("/")}>Go Home</button>
        </div>
    )
}
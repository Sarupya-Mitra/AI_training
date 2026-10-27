import { useAuth } from "../context/AuthContext"; 

export default function About(){
    const {user} = useAuth()
    return (
        <div className="container">
            <h1> About Page </h1>
            <p>Protected About Page</p>
            <p> Welcome, {user.email}</p>
        </div>
    );
}
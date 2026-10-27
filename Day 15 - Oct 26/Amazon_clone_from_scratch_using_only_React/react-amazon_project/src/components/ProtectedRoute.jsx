import {Navigate,Outlet,useLocation} from "react-router-dom"
import { useAuth } from "../context/AuthProvider";

export default function ProtectedRoute(){
    const {user} = useAuth();
    const location = useLocation();
    if(!user){
        return (
            <Navigate to="/login" state={{from : location}} replace />
        )
    }

    return <Outlet />
}
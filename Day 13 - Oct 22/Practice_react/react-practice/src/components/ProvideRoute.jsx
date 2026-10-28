import { useAuth } from "../context/AuthProvider";
import { Navigate, replace,Outlet } from "react-router-dom";
import { useLocation } from "react-router-dom";

export  function ProvideRoute(){
    const {user,login} = useAuth()
    const location = useLocation()
    if(!user){
        return (
        <Navigate to={"/login"} state={{from : location}} replace/>
        )
    }
    return <Outlet/>
}
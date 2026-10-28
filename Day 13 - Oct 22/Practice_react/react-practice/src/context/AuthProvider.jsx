import { createContext,useContext,useState } from "react";
const LoginContext = createContext()
export function AuthProvider({children}){
    const [user,setUser] = useState(()=>
    {
        const savedUser = sessionStorage.getItem("user");
        return savedUser? JSON.parse(savedUser):null;
     })

    function login(email,pwd){
        if(email === "admin@sample.com" && pwd==="sample123"){
            const loggedinUser = {email};
            sessionStorage.setItem("user",JSON.stringify(loggedinUser))
            setUser(loggedinUser);
            return true;
        }
        return false;
    }

    function logout()
    {
        sessionStorage.removeItem("user")
        setUser(null)
    }
    return (
        <LoginContext.Provider value={{user,login,logout}}>{children}</LoginContext.Provider>
    )
}

export function useAuth(){
    return useContext(LoginContext)
}
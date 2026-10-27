import {createContext,useState,useContext} from "react"

const AuthContext = createContext();

export function AuthProvider({children}){
    const [user,setUser] = useState(()=>{
        const savedUser = sessionStorage.getItem("user");
        return savedUser? JSON.parse(savedUser) : null;
    });

    function login(email,pwd){
        // Just demo credentials
        if(email === "admin@example.com" && pwd === "1234"){
            const loggedInUser = {email};
            sessionStorage.setItem("user",JSON.stringify(loggedInUser));
            setUser(loggedInUser);
            return true;
        }
        return false;
    }

    function logout(){
        sessionStorage.removeItem("user");
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{user,login,logout}}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(){
    return useContext(AuthContext);
}

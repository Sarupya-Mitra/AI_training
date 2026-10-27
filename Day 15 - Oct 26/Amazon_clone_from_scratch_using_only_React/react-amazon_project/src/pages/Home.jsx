import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthProvider"
export default function Home({products}){
    const {user} = useAuth()
    let logintext = ""
    if(!user){
        logintext = "You are not logged in"
    }
    else{logintext = `Welcome ${user.email}`}
    return (
        <div>
            <h2> Home Page : </h2>
            {products.map((product) => 
                (<div key={product.id}>
                <Link to={`/products/${product.id}`}>{product.id} - {product.name}</Link>
                </div>
            ))}
        <footer>
            <p>{logintext}</p>
        </footer>
        </div>
    )
}
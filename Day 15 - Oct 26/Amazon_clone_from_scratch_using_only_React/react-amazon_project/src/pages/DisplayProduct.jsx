import { useParams,useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { use } from "react";
import { useAuth } from "../context/AuthProvider";

export default function DisplayProduct({products}){
    const {id} = useParams()
    const navigate = useNavigate()
    const {cart,addtocart} = useCart()

    const product = products.find((product) => product.id == Number(id))

    function handleAddtoCart(product){
       
        addtocart(product)
    }

    const {user} = useAuth()
    let logintext = ""
    if(!user){
        logintext = "You are not logged in"
    }
    else{logintext = `Welcome ${user.email}`}
    
    return(
        <div key={product.id}>
            <p>Name : {product.name}</p>
            <p>Price : {product.price}</p>
            <button onClick={()=> navigate("/")}>Go Back</button>
            <button onClick={() => handleAddtoCart(product)}>Add to Cart</button>

            <footer>{logintext}</footer>
        </div>
        
    )
}
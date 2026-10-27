import { useAuth } from "../context/AuthProvider";
import { useCart } from "../context/CartContext";
import { useNavigate } from "react-router-dom";

export default function DisplayCart(){
    const {cart} = useCart()
    const navigate = useNavigate()
    const total = cart.reduce(
        (sum,product) => sum + product.price, 0 
    )
    const {user} = useAuth()
    let logintext = ""
    if(!user){
        logintext = "You are not logged in"
    }
    else{logintext = `Welcome ${user.email}`}

    return (
        <div>
        {cart.map((product) => 
            (<div key={product.id}>
                <p>{product.name} - Rs.{product.price}</p>
            </div>)
        )}
        <p>Your Total Amount : {total}</p>
        <button onClick={()=>navigate("/payment")}>Proceed to Pay</button>

        <footer>{logintext}</footer>

        </div>
        
    )

}
// function Product(props){
//   return(
//     <div>
//       <h2>Name: {props.name}</h2>
//       <p>Price : {props.price}</p>
//     </div>
//   )
// }
import {useState} from "react"

function Product(props){
    const [count,setCount] = useState(0) // variable and a function
    return (
        <div>
            <h2>{props.name}</h2>
            <p>Price : {props.price}</p>
            <button onClick={() => setCount(count + 1)}>
                Add to Cart 
            </button>
            <p> Quantity : {count}</p>
        </div>
    )
}
export default Product
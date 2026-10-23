import { useParams,useNavigate } from "react-router-dom";
import {useState} from "react";
function DeleteParticularProduct({products}){
    const {id} = useParams()
    const product = products.find((product)=> product.id == Number(id))
    const navigate = useNavigate()

    const [name,setName] = useState(product.name)
    const [price,setPrice] = useState(product.price)
    const [image,setImage] = useState(product.image)



    function deleteproduct(event){
        event.preventDefault()

        const deletedproduct = {
        "id" : Number(id),
        "name" : name,
        "price" : Number(price),
        "image" : image
    }

        fetch(`http://127.0.0.1:8000/products/${id}`, {method : "DELETE", headers:{"Content-Type": "application/json"},
        body : JSON.stringify(deletedproduct)})
        .then((response) => (response.json()))
        .then(()=>(navigate("/products")))
    }

    return (
        <div>
            <h2>Are you sure you want to delete the following product?</h2>
            <input type="number" value={id} disabled></input><br/>
            <input type="text" value={name} disabled></input><br/>
            <input type="number" value={price} disabled></input><br/>
            <input type="text" value={image} disabled></input><br/>

            <button onClick={deleteproduct}>DELETE</button><br/>
            <button onClick={()=>(navigate("/products"))}>Back to Products</button>

        </div>
    )


}
export default DeleteParticularProduct
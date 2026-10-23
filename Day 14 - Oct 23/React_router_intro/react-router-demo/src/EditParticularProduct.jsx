import { useParams,useNavigate } from "react-router-dom";
import {useState} from "react";

function EditParticularProduct({products}){
    const {id} = useParams()
    const navigate = useNavigate()
    const product = products.find((product) => product.id == Number(id))

    const [name, setName] = useState(product.name)
    const [price, setPrice] = useState(product.price)
    const [image, setImage] = useState(product.image)

    function editproduct(event){
        event.preventDefault()

        const updatedproduct = {
            id: Number(id),
            name: name,
            price: Number(price),
            image: image
        }

        fetch(`http://127.0.0.1:8000/products/${id}`,{method : "PUT",
            headers : {"Content-Type": "application/json"},body : JSON.stringify(updatedproduct)})
            .then((response) => response.json())
            .then(()=> {navigate("/products")})
    }
    return (
        <div>
            <p>Editing product with {product.id}</p>

        <form onSubmit={editproduct}>
        {/* <input type="number" placeholder="Product ID" value={id}
          onChange={(e) => setId(e.target.value)}
        /> */}

        <br />

        <input type="text" placeholder="Product Name" value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <br />

        <input type="number" placeholder="Price" value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <br />

        <input type="text" placeholder="Image URL" value={image}
          onChange={(e) => setImage(e.target.value)}
        />

        <br />

        <button type="submit">
          Save Product
        </button>
      </form>

        </div>
    )
}

export default EditParticularProduct
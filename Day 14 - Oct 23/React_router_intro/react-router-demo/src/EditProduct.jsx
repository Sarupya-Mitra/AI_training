import {Link} from "react-router-dom"

function EditProduct({products}){
    
    return(
        <div>
            <h2>Select the product you want to edit: </h2>
            {products.map((product) => (
                <div key={product.id}>
                    <Link to={`/edit-particular-product/${product.id}`}>
                    {product.name}
                    </Link>
                </div>
            ))}
        </div>
    )
}

export default EditProduct
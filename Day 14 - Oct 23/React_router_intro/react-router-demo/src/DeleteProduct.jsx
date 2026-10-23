import {Link} from "react-router-dom"
function DeleteProduct({products}){
    return (
        <div>
            <h2>Select which product to delete:</h2>
            {products.map((product) =>
                (<div key={product.id}>
                    <Link to={`/delete-particular-product/${product.id}`}>{product.name}</Link>
                </div>))
            }
        </div>
    )
}
export default DeleteProduct
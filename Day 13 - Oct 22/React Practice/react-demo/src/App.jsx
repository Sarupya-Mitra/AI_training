import Product from "./Product"
import "./App.css"
import {useEffect,useState} from "react"

// function App(){
//   return(
//     <div>
//       <h1>Products:</h1>
//       <Product name="Wireless Mouse" price="1200" />
//       <Product name="Keyboard" price = "1000"/>
//       <Product name="Monitor" price = "20000" />
//     </div>
//   )
// }
////////////////////////////////////////// map()
// function App(){
//   const products = [
//     {id:1,name:"Wireless Mouse",price:1200},
//     {id : 2,name : "Keyboard" , price : 1000},
//     {id : 3, name : "Monitor",price:20000}
//   ]

//   return (
//     <div>
//       <h1>Product List</h1>
//       {products.map((product) => (
//         <Product 
//         key = {product.id}
//         name = {product.name}
//         price = {product.price}
//         />
//       ))}
//     </div>
//   )
// }

////////////////////////////////////////////////// Adding a 'add product' button and text boxes
// function App() {
//   const [products, setProducts] = useState([
//     { id: 1, name: "Wireless Mouse", price: 1200 },
//     { id: 2, name: "Keyboard", price: 2500 },
//     { id: 3, name: "Monitor", price: 12000 }
//   ])

//   const [name, setName] = useState("")
//   const [price, setPrice] = useState("")

//   function addProduct(event) {
//     event.preventDefault()   // Tells html to not do its default action, i.e don't reload the entire page.
//     // Instead we will only reload the part of the page that is getting updated.
//     const newProduct = {
//       id: products.length + 1,
//       name: name,
//       price: price
//     }

//     setProducts([...products, newProduct])  // Appending newProduct to products (... means spreader function, it determines whether I 
//                                       //// append or overwrite; if I don't write ... then products array will be overwritten by newProduct)

//     setName("")
//     setPrice("")
//   }

//   return (
//     <div>
//       <h1>Product List</h1>

//       <input
//         type="text"
//         placeholder="Product name"
//         value={name}
//         onChange={(e) => setName(e.target.value)}  // e means event, e.target means the input tag
//       />

//       <input
//         type="number"
//         placeholder="Price"
//         value={price}
//         onChange={(e) => setPrice(e.target.value)}
//       />

//       <button onClick={addProduct}>
//         Add Product
//       </button>

//       {products.map((product) => (
//         <Product
//           key={product.id}
//           name={product.name}
//           price={product.price}
//         />
//       ))}
//     </div>
//   )
// }
//////////////////////////////////////////////  Connecting react to api
// function App() {
//   const [products, setProducts] = useState([])

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/products")  // fetching data from API
//       .then((response) => response.json())  // convert response to json
//       .then((data) => {
//         setProducts(data)  // Every data is passed to setProducts function
//       })
//       .catch((error) => {
//         console.error("Error fetching products:", error)
//       })
//   }, [])

//   return (
//     <div>
//       <h1>Product Store</h1>

//       {products.map((product) => ( // Here we didn't use the Product component, we directly use HTML.
//         <div key={product.id}>    
//           <img
//             src={product.image}
//             alt={product.name}
//             width="180"
//           />

//           <h2>{product.name}</h2>
          
//           <p>Price: ₹{product.price}</p>

//           <hr />
//         </div>
//       ))}
//     </div>
//   )
// }


function App() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    fetch("http://127.0.0.1:8000/products")  // fetching data from API
      .then((response) => response.json())  // convert response to json
      .then((data) => {  // data is the json we got by converting response to json
        setProducts(data)  // the entire data(list of products in this example) is passed to setProducts function and so 
        // products get overwritten with the data. 
      })
      .catch((error) => {
        console.error("Error fetching products:", error)
      })
  }, [])

  const [name,setName] = useState("")
  const [price,setPrice] = useState("")
  const [image,setImage] = useState("")
  

  function addProduct(event){
    event.preventDefault()

    const newProduct={id:products.length + 1,name : name,price : price,image : image}
    fetch("http://127.0.0.1:8000/products",
      {
        method:"POST",      
        headers: {
        'Content-Type': 'application/json',
        },
       body : JSON.stringify(newProduct),
      }
    )
    .then((response) =>{
      if(!response.ok){throw new Error("Failed to add product");}
      return response.json();
    })
    .then((savedproduct) => {
    setProducts([...products,newProduct])
    setName("")
    setImage("")
    setPrice("")
    })
    .catch((error)=> {console.error("Error posting product",error)})
  }

  return (
    <div>
      <h1>Product Store</h1>
      <input type="text" placeholder="Product Name" value={name} onChange={(e)=> setName(e.target.value)}/>
      <input type="text" placeholder="Product Price" value={price} onChange={(e)=> setPrice(e.target.value)} />
      <input type="text" placeholder="Product Image URL" value={image} onChange={(e)=> setImage(e.target.value)} />
      <button onClick={addProduct}>Add Product</button>

      {products.map((product) => ( // Here we didn't use the Product component, we directly use HTML.
      // the key attribute seen below is special case for React, it helps React to understand which element has changed
      // and render only that changed element, and doesn't re-render the others. So here when a new product is added, only that 
      // element is rendered fresh and the rest are not re-rendered, they are already present in the webpage.
        <div key={product.id}>     
          <img
            src={product.image}
            alt={product.name}
            width="180"
          />

          <h2>{product.name}</h2>
          
          <p>Price: ₹{product.price}</p>

          <hr />
        </div>
      ))}
    </div>
  )
}





export default App
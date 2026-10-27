import { createContext,useContext,useEffect,useState } from "react";

const CartContext = createContext();

export function CartProvider({children}){
    const [cart,setCart] = useState(()=>
    {
        const savedcart = sessionStorage.getItem("cart")
        return savedcart? JSON.parse(savedcart) : [];
    })

    useEffect(() => sessionStorage.setItem("cart",JSON.stringify(cart)))
    // Whenver cart will be changed then due to useEffect the session variable
    // will also change, because when cart changes React detects the change and
    // it will run the useEffect.

    function addtocart(newproduct){
        setCart((cart) => [...cart,newproduct])
    }

    return (
        <CartContext.Provider value={{cart,addtocart}}>{children}</CartContext.Provider>
    )
}

export function useCart(){
    return useContext(CartContext)
}
import { useNavigate } from "react-router-dom";

export default function Payment(){
    const navigate = useNavigate()
    return (<div>Payment Page<br></br>
        <button onClick={()=> navigate("/")}>Go Home</button>
    </div>)
}
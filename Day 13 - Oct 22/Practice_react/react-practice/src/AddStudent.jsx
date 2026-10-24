import {useState} from "react"
import { useNavigate } from "react-router-dom"


function AddStudent({students}){
    const navigate = useNavigate()
    const [name,setName] = useState("")
    const [age,setAge] = useState("")
    const [standard,setStandard] = useState("")

    function addtodb(event){
        event.preventDefault();
        
        const newStudent = {
            student_id : students.length + 1,
            name : name,
            age : Number(age),
            standard : Number(standard)
        }
        fetch("http://127.0.0.1:8000/students",
            {
                method : "POST", headers : {"Content-Type" : "application/json"},
                body : JSON.stringify(newStudent)
            }
        )
        .then((response) => {if(!response.ok){throw new Error('Post Request Failed')}
                               return response.json()})
        .then(()=> navigate("/students"))
        .catch((error) => console.log(error))
    }

    return (
        <div>
            <form onSubmit={addtodb}>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)}
                placeholder="Name"/> <br/>
                <input type="number" value={age} onChange={(e) => setAge(e.target.value)}
                placeholder="Age"/> <br/>
                <input type="number" value={standard} onChange={(e) => setStandard(e.target.value)}
                placeholder="Standard"/> <br/>      
                <button type="submit">Submit</button>          
            </form>
        </div>
    )

}
export default AddStudent
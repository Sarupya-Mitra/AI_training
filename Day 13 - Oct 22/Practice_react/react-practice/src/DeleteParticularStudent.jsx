import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

export default function DeleteParticularStudent({students}){
    const {id} = useParams()
    const navigate = useNavigate()
    const student = students.find((student) => student.student_id == Number(id))

    // const [name,setName] = useState(student.name)
    // const [age,setAge] = useState(student.age)
    // const [standard,setStandard] = useState(student.standard)
    function handledelete(){
        fetch(`http://127.0.0.1:8000/students/${id}`,{
            method:"DELETE"
        }).then((response) => {if(!response.ok) {throw new Error("Can't perform deletion")}
        return response.json()})
        .then(()=>navigate("/students"))
        .catch((error) => console.log(error))
    }
    return (
        <div>
            <h2>Are you sure you want to delete the following student?</h2>
            <p>Name : {student.name}, age : {student.age}, standard : {student.standard}</p>
            <button onClick={handledelete}>DELETE</button>
        </div>
    )
}
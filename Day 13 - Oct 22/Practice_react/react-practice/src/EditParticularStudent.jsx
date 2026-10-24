import { useState } from "react";
import { useParams,useNavigate } from "react-router-dom";
function EditParticularStudent({students}){
    const {id} = useParams()
    const navigate = useNavigate()
    const student = students.find((student) => student.student_id == Number(id))

    const [name,setName] = useState(student.name)
    const [age,setAge] = useState(student.age)
    const [standard,setStandard] = useState(student.standard)

    function edit_db(event){
        event.preventDefault()

        const modifiedStudent = {
            student_id : Number(id),
            name : name,
            age : Number(age),
            standard : Number(standard)
        }

        fetch(`http://127.0.0.1:8000/students/${id}`, {
            method:"PUT", headers : {"Content-Type" :  "application/json"},
            body : JSON.stringify(modifiedStudent)
        }).then((response) => { if(!response.ok){throw new Error("Update not possible")} return response.json()})
        .then(()=> navigate("/students"))
        .catch((error) => (console.log(error)))
    }

    return (
        <div>
            <h2>Update the Details:</h2>
            <form onSubmit={edit_db}>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)}></input><br/>
                <input type="number" value={age} onChange={(e) => setAge(e.target.value)}/><br/>
                <input type="number" value={standard} onChange={(e) => setStandard(e.target.value)}/><br/>
                <button type="submit">Submit</button>
            </form>

        </div>
    )

}

export default EditParticularStudent
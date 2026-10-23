import "./App.css"
import Students from "./Students.jsx"
import {useEffect,useState} from "react"

function App(){
    const[students,setStudents] = useState([])
    useEffect(()=> {
        fetch("http://127.0.0.1:8000/students")
            .then((response) => response.json())
            .then((data) => setStudents(data))
            .catch((error) => {console.log("Error : ",error)})
    })
    const[name,setName] = useState("")
    const[age,setAge] = useState("")
    const[standard,setStandard] = useState("")

    function addStudent(event){
        event.preventDefault()
        const newStudent = {student_id : students.length + 1, name : name,age: age, standard : standard}
        fetch("http://127.0.0.1:8000/students", {method : "POST",body : JSON.stringify(newStudent),})
        .then((response) => {
            if (!response.ok) {throw new Error("Failed to add new student");}
            return response.json();})
        .then((savedstudent)=> {
            setStudents([...students,newStudent])
            setName("")
            setAge("")
            setStandard("")
        })
        .catch((error) => {console.log("Error Occurred: ",error)})
    }
    return(
        <div>
            <input type="text" placeholder="Enter Name" value = {name} onChange={(e) => setName(e.target.value)}></input>
            <input type="number" placeholder="Enter Age" value = {age} onChange={(e)=>setAge(e.target.value)}></input>
            <input type="number" placeholder = "Enter Standard" value = {standard} onChange={(e) => setStandard(e.target.value)}></input>
            <button onClick={addStudent}>Add Student</button>
            {students.map((student) => (
                <div key={student.student_id}>
                    <Students name={student.name} age={student.age} standard={student.standard}/>
                    <br></br>
                </div>
            ))}
        </div>
    )
}

export default App
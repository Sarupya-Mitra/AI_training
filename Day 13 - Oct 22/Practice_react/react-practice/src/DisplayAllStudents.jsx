import Students from "./Students";
function DisplayAll({students}){
return (
        <div>
            {/* <input type="text" placeholder="Enter Name" value = {name} onChange={(e) => setName(e.target.value)}></input>
            <input type="number" placeholder="Enter Age" value = {age} onChange={(e)=>setAge(e.target.value)}></input>
            <input type="number" placeholder = "Enter Standard" value = {standard} onChange={(e) => setStandard(e.target.value)}></input> */}
            {/* <button onClick={addStudent}>Add Student</button> */}
            {students.map((student) => (
                <div key={student.student_id}>
                    <Students name={student.name} age={student.age} standard={student.standard}/>
                    <br></br>
                </div>
            ))}
        </div>
    )
}

export default DisplayAll
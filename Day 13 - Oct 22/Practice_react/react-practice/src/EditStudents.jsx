import { Link } from "react-router-dom";

function EditStudents({students}){
    return (
        <div>
            <h2> Select which student you want to edit</h2>
        
            {students.map((student) => (
                <div key={student.student_id}>
                    <Link to={`/edit-particular-student/${student.student_id}`}>{student.student_id} - {student.name}</Link>
                </div>
            ))}
        </div> 
    )
}

export default EditStudents
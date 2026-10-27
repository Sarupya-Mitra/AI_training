import { Link } from "react-router-dom";
export default function DeleteStudents({students}){
    return (
        <div>
            <h2>Select which student you want to delete: </h2>
            {students.map((student) => (
                <div key={student.student_id}>
                    <Link to={`/delete-particular-student/${student.student_id}`}>
                        {student.student_id} - {student.name}
                    </Link>
                </div>
            ))}
        </div>
    )
}
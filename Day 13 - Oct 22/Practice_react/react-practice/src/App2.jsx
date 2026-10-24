import "./App.css"
import DisplayAll from "./DisplayAllStudents.jsx"
import Home from "./Home.jsx"
import AddStudent from "./AddStudent.jsx"
import {useEffect,useState} from "react"
import {BrowserRouter,Routes,Route,Link,useParams,useNavigate} from "react-router-dom"
import EditStudents from "./EditStudents.jsx"
import EditParticularStudent from "./EditParticularStudent.jsx"

function App(){
    const[students,setStudents] = useState([])
    useEffect(()=> {
        fetch("http://127.0.0.1:8000/students")
            .then((response) => response.json())
            .then((data) => setStudents(data))
            .catch((error) => {console.log("Error : ",error)})
    })

    return(
        <BrowserRouter>
            <nav>
                <Link to="/">Home</Link>
                {" | "}
                <Link to="/students">All Students</Link>
                {" | "}
                <Link to="/add-student">Add Student</Link>
                {" | "}
                <Link to={"/edit-student"}>Edit Student</Link>
            </nav>
            <Routes>
                <Route path="/"  element={<Home />}/>
                <Route path="/students" element={<DisplayAll students={students}/>}/>
                <Route path="/add-student" element={<AddStudent students={students}/>}/>
                <Route path="/edit-student" element = {<EditStudents students={students}/>}/>
                <Route path="/edit-particular-student/:id" element={<EditParticularStudent students={students}/>} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
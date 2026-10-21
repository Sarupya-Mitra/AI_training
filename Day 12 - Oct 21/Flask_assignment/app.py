from flask import Flask,jsonify,request
from pydantic import BaseModel

app = Flask(__name__)

# class Student(BaseModel):
#     id: int
#     name : str
#     course : str
#     score : int

students = [
{
"id": 1,
"name": "Rhea Kapoor",
"course": "Python",
"score": 82
},
{
"id": 2,
"name": "Zain Malik",
"course": "SQL",
"score": 76
},
{
"id": 3,
"name": "Devika Rao",
"course": "Cloud",
"score": 91
}
]

### 1. Get all students
@app.route("/students")
def get_all_students():
    return jsonify(students)

### 2. Get student by ID
@app.route("/students/<int:student_id>")
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"message": "Student not found"}),404

### 3. Add a student
@app.route("/students" , methods = ['POST'])
def add_student():
    student = request.get_json()
    students.append(student)
    return jsonify({"message": "Student added successfully"})

### 4. Update a student
@app.route("/students/<int:student_id>",methods = ['PUT'])
def update_student(student_id):
    for student in students:
        if student["id"] == student_id:
            new_student = request.get_json()
            for field in new_student:
                if field != "id":
                    student[field] = new_student[field]
            return jsonify({"message": "Student updated successfully"})
    return jsonify({"message": "Student not found"}),404

### 5. Deleting a student
@app.route("/students/<int:student_id>",methods=['DELETE'])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "Student deleted successfully"})
    return jsonify({"message": "Student not found"}),404




if __name__ == "__main__":
    app.run(debug=True)
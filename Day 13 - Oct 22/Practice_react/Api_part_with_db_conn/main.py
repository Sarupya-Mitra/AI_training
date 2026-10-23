import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

def get_conn():
    conn = psycopg2.connect(
        host = "localhost",
        dbname = "a_practice_student",
        user = "postgres",
        password = "Admin@123"
    )
    return conn

@app.get("/students")
def get_students():
    students = []
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("Select * from students")
    rows = cursor.fetchall()
    for row in rows:
        student = {
            "student_id":row[0],
            "name":row[1],
            "age":row[2],
            "standard" : row[3]
        }
        students.append(student)
    cursor.close()
    conn.close()
    return students

@app.post("/students")
def insert_student(student: dict):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (student_id, name, age, standard) "
                   "VALUES (%s, %s, %s, %s)",
                   (student["student_id"], student["name"], student["age"], student["standard"]))
    conn.commit()
    cursor.close()
    conn.close()
    return student
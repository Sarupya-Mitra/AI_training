from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id : int
    title : str
    status : str

tasks = [{"id" : 1 , "title" : "Prepare Report" , "status" : "Pending"},
         {"id" : 2 , "title" : "Review Invoice" , "status" : "Completed"},
         {"id" : 3 , "title" : "Update Dashboard" , "status" : "Pending"}]

@app.get("/tasks")
def get_tasks():
    return {"message" : "Tasks found ",
            "tasks" : tasks}

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            return {"message" : "Task found ","task" : task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def insert_task(task : Task):
    tasks.append(task.model_dump())  # since task is a Task object, we need to convert it to
    # dict before appending because at the top we have appended dict objects to tasks
    return {"message" : "Task added successfully","task" : task}

@app.put("/tasks/{task_id}")
def update_task(task_id : int, new_task : Task):
    for task in tasks:
        if task["id"] == task_id:
            task['title'] = new_task.title
            task["status"] = new_task.status
            return {"message" : "Task updated successfully","task" : task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message" : "Task deleted successfully","task" : task}

    raise HTTPException(status_code=404, detail="Task not found")




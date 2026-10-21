from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200  ### 2. Assert for 200 status code
    assert isinstance(response.json()["tasks"],list) ### 3. assert for list

def test_get_task_by_id():
    response = client.get("/tasks/1")
    ### 4 asserts for 200 status code and id=1
    assert response.status_code == 200
    assert response.json()["task"]["id"] == 1

## 6. Test for post
def test_insert_task():
    response = client.post("/tasks",
                           json = {"id" : 4 , "title" : "Check server logs" ,
                                   "status" : "Pending"})
    assert response.status_code == 200
    assert response.json()["task"]["id"] == 4
    assert response.json()["task"]["title"] == "Check server logs"

## 7. Test for invalid post
def test_insert_task_invalid():
    response = client.post("/tasks",
                           json = {"id" : 4 , "title" : "Check server logs" })
    assert response.status_code == 422


## 8. Test for put
def test_update_task():
    response = client.put("/tasks/2",json =
                          {"id" : 2 , "title" : "Review Invoice" , "status" : "Completed"})
    assert response.status_code == 200
    assert response.json()["task"] == {"id" : 2 , "title" : "Review Invoice" , "status" : "Completed"}

# 9. Test for delete
# def test_delete_task():
#     response = client.delete("tasks/3")
#     assert response.status_code == 200

## 10. Test for get after delete
def test_get_after_delete():
    response = client.delete("/tasks/3")
    assert response.status_code == 200
    response = client.get("/tasks/3")
    assert response.status_code == 404


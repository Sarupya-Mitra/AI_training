from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message" : "Hello World"}

@app.get("/hello/{name}")
def hello(name:str):
    return {"message" : f"Hello {name}"}


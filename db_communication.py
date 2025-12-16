from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def test():
    return{"message":"Heelo, world"}
@app.get("/ahmed")
def test1():
    return{"message":"This is test1 endpoint"} 

students = {1:"aroush", 2:"ahmed", 3:"sara"}
@app.get("/students")
def get_students():
    return students

@app.get("/students/{stud_id}")
def student_search(stud_id:int):
    return {"id":stud_id,"name":students[stud_id]}

@app.get("/add_student")
def add_student(stud_id:int,name:str):
    students[stud_id] = name
    return students
## http://127.0.0.1:8000/add_student?stud_id=4&name=razia another way to add data into dictionary using query parameters

def add_students(stud_id1:int,stud1_name:str):
    students[stud_id1]=stud1_name
    students
@app.post("/add_student_diff1")
def add_student_diff():
    students['new_id']="new_name"
    return students
from pydantic import BaseModel
class newdata(BaseModel):
    stud_id:int
    name:str
@app.post("/add_student_dict")  
def add_data(newdata:newdata):
    students[newdata.stud_id]=newdata.name
    return  students
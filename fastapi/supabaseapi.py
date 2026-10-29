import os

from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/students")
def get_students():
    response = client.table("students").select("*").execute()
    return response.data

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    response = client.table("students").select("*").eq("id", student_id).execute()
    return response.data

@app.get("/students/age/{age}")
def filter_by_age(age: int):
    response = client.table("students").select("*").eq("age", age).execute()
    return response.data

# this library is used for validations
from pydantic import BaseModel, Field, EmailStr


#this is validation of the input data
class Student(BaseModel):
    name : str 
    email : EmailStr    
    age : int
    course : str


@app.post("/students/insert")
def insert_student(student: Student):
    response = client.table('students').insert(student.dict()).execute()
    return response.data


# GET  → data lena
# POST → data bhejna/create karna

class Student(BaseModel):
    name : str = Field(min_lenth=5, max_length=100)
    email : EmailStr 
    age : int = Field(ge=18, le=100)
    course : str


@app.put("/students/update/{student_id}")
def update_student(student_id: int, student: Student):
    response = client.table("students").update(student.dict()).eq("id", student_id).execute()
    return response.data

#@app.put()       → FastAPI PUT endpoint
#def              → Python function
#student_id       → path parameter
#Student          → Pydantic class/model
#table("students")→ database table
#update()         → update method
#eq()             → filter (=)  # where 
#execute()        → query execute
#response.data    → returned data


# Patch

class studentpatch(BaseModel):
    name : str | None = Field(default=None, min_length=5, max_length=100)
    email: EmailStr | None = Field(default=None)
    age: int | None = Field(default=None, ge=18, le=100)
    course: str | None = Field(default=None)


@app.patch("/students/patch/{student_id}")
def student_patch(student_id: int, student: studentpatch):
    response = client.table("students").update(
        student.model_dump(exclude_unset=True)
    ).eq("id", student_id).execute()

    return response.data



# delete
class Student_delete(BaseModel):
    name : str | None = Field(min_length=5, max_length=100)
    mail : str | None = Field(default=None)
    age : int | None = Field(default=100, ge=18, le=100)
    course : int | None = Field(default=None)

@app.delete("/student/delete/{student_id}")
def student_del(student_id: int):
    response = client.table("students").delete().eq('id', student_id).execute()
    return response.data


# pip install slowapi


from slowapi import Limiter
from fastapi import Request
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


@app.get("/studentslimit/xyz")
@limiter.limit("5/minute")
def limit_student_update(request:Request):
    response = client.table("students").select("*").execute()
    return response.data


# CORSE - Cross - origin resource sharing
# frontend : localhost/5000
# backend api part : localhost/5004

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,

    allow_origins=["http://localhost:3000","http://127.0.0.1:5004"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/test-cors")
def test_cors():

    return {
        "message": "CORS is working!"
    }



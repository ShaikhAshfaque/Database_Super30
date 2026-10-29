```python
# ============================================================
# FASTAPI + SUPABASE : 5 HTTP METHODS
# GET, POST, PUT, PATCH, DELETE
# ============================================================

# 1. IMPORTS
from fastapi import FastAPI
from pydantic import BaseModel, Field

# FastAPI application create karna
app = FastAPI()

# NOTE:
# Supabase ka "client" pehle se configure hona chahiye.
# Example:
# client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# PYDANTIC MODEL
# ============================================================

class Student(BaseModel):
    # POST aur PUT ke liye required fields
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=1, le=100)
    course: str


# PATCH ke liye alag model
# Ismein sabhi fields optional hain.
class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    course: str | None = None


# ============================================================
# 1. GET METHOD : DATA READ KARNA
# ============================================================

@app.get("/students")
def get_students():

    # Supabase ke students table ko access karo
    # select("*") ka matlab saare columns select karna
    # execute() query ko database par run karta hai
    response = (
        client.table("students")
        .select("*")
        .execute()
    )

    # Sirf actual database records return karo
    return response.data


# ============================================================
# 2. POST METHOD : NAYA STUDENT CREATE KARNA
# ============================================================

@app.post("/students")
def create_student(student: Student):

    # student: Student request body ko validate karta hai
    # student.name, student.age aur student.course
    # request JSON se values receive karte hain

    response = (
        client.table("students")
        .insert({
            "name": student.name,
            "age": student.age,
            "course": student.course
        })
        .execute()
    )

    # Inserted record return karo, agar response mein available ho
    return response.data


# ============================================================
# 3. PUT METHOD : POORE EDITABLE RECORD KO UPDATE KARNA
# ============================================================

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    # {student_id} URL se ID receive karta hai
    # Example: PUT /students/5
    # Yahan student_id = 5 hoga

    response = (
        client.table("students")
        .update({
            "name": student.name,
            "age": student.age,
            "course": student.course
        })
        # Sirf us record ko update karo jiska id match ho
        .eq("id", student_id)
        .execute()
    )

    # Updated records return karo, agar available hon
    return response.data

    # NOTE:
    # PUT request mein saare editable fields bhej rahe hain.
    # Supabase ka update() specified columns update karta hai;
    # ye apne aap record replacement perform nahi karta.


# ============================================================
# 4. PATCH METHOD : SIRF KUCH FIELDS UPDATE KARNA
# ============================================================

@app.patch("/students/{student_id}")
def patch_student(student_id: int, student: StudentUpdate):

    # Sirf wahi fields dictionary mein rakho
    # jo request body mein actually bheji gayi hain
    data = student.model_dump(exclude_unset=True)

    # Example request:
    # {"course": "GenAI"}
    #
    # data banega:
    # {"course": "GenAI"}
    #
    # Name aur age update nahi honge

    # Agar empty JSON {} aaye toh update mat karo
    if not data:
        return {"message": "No fields provided for update"}

    response = (
        client.table("students")
        .update(data)
        # Matching student ID ka record hi update hoga
        .eq("id", student_id)
        .execute()
    )

    # Updated records return karo, agar available hon
    return response.data

    # NOTE:
    # Optional fields ke liye str | None = None use hua hai.
    # exclude_unset=True omitted fields ko remove karta hai.
    # Explicit null bhejne par field payload mein reh sakti hai.


# ============================================================
# 5. DELETE METHOD : STUDENT DELETE KARNA
# ============================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    # URL se student ID receive hogi
    # Example: DELETE /students/5

    response = (
        client.table("students")
        .delete()
        # Sirf matching ID wala record target karo
        .eq("id", student_id)
        .execute()
    )

    # Confirmation message return karo
    return {
        "message": "Delete request executed",
        "data": response.data
    }

    # NOTE:
    # Database permissions aur Supabase policies ke hisaab se
    # operation successful ya unsuccessful ho sakta hai.
    # Production mein deletion confirm karna aur errors handle
    # karna bhi zaroori hai.


# ============================================================
# QUICK REVISION : CRUD
# ============================================================

# CREATE  -> POST   -> .insert(data)
# READ    -> GET    -> .select("*")
# UPDATE  -> PUT    -> .update(data)
# PARTIAL -> PATCH  -> .update(partial_data)
# DELETE  -> DELETE -> .delete()

# PUT / PATCH / DELETE mein .eq("id", student_id)
# specific student record ko target karta hai.

# IMPORTANT:
# Table ka naam "students" database mein exist karna chahiye.
# Client, Supabase URL aur key separately configure hone chahiye.
# Production mein service-role key ko kabhi expose mat karna.
```
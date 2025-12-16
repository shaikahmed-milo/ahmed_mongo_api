from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Your existing DB configuration
db_url = "postgresql://neondb_owner:npg_BPpxa8uljv2M@ep-holy-moon-ah56og23-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

class Students(BaseModel):
    id: int
    name: str
    age: int

# Use this for update requests (ID is optional because it comes from the URL)
class StudentUpdate(BaseModel):
    name: str
    age: int

def get_connection_url():
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn 

# --- YOUR EXISTING CREATE ---
@app.post("/students/data/db")
def store_data_db(student : Students):
    conn = get_connection_url()
    try:
        cursor = conn.cursor()
        insert_query = "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (student.id, student.name, student.age))
        conn.commit()
        return {"message": "Student data saved to database successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # ALWAYS close connection, even if error happens
        if conn: conn.close()

# --- NEW: UPDATE (PUT) ---
@app.put("/students/data/db/{student_id}")
def update_student_db(student_id: int, student: StudentUpdate):
    conn = get_connection_url()
    try:
        cursor = conn.cursor()
        
        # 1. The SQL Query
        update_query = "UPDATE student SET name = %s, age = %s WHERE id = %s"
        
        # 2. Execute with parameters
        cursor.execute(update_query, (student.name, student.age, student_id))
        conn.commit()
        
        # 3. Validation: Check if any row was actually touched
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {"message": "Student updated successfully"}
    finally:
        if conn: conn.close()

# --- NEW: DELETE (DELETE) ---
@app.delete("/students/data/db/{student_id}")
def delete_student_db(student_id: int):
    conn = get_connection_url()
    try:
        cursor = conn.cursor()
        
        # 1. The SQL Query
        delete_query = "DELETE FROM student WHERE id = %s"
        
        # 2. Execute
        cursor.execute(delete_query, (student_id,))
        conn.commit()
        
        # 3. Validation
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {"message": "Student deleted successfully"}
    finally:
        if conn: conn.close()
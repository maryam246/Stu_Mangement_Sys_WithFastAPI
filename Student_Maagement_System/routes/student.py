# routes/student.py
from fastapi import APIRouter, HTTPException, Depends
from bson.objectid import ObjectId
from Database.schemas import all_students, individual_data
from Database.models import Student
from utils.config import collection
from utils.auth import get_current_admin
from utils.validation import validate_program_department
from utils.id_generator import generate_student_id

router = APIRouter()

# Create a new student record (only accessible by logged-in admins)
@router.post("/create")
async def create_student(new_student: Student, current_admin: dict = Depends(get_current_admin)):
    try:
        # Validate program and department compatibility
        validate_program_department(new_student.program, new_student.department)

        # Generate student ID using the campus ID of the current admin
        student_id = generate_student_id(current_admin["campus_id"])

        new_student_dict = new_student.dict()
        new_student_dict["student_id"] = student_id
        new_student_dict["admin_id"] = current_admin["email"]
        new_student_dict["campus"] = current_admin["campus"]
        collection.insert_one(new_student_dict)
        return {"status_code": 200, "message": "Student record created successfully", "student_id": student_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail="An error occurred while creating the student record")

# Get all students created by the logged-in admin
@router.get("/get-all")
async def get_all_students(current_admin: dict = Depends(get_current_admin)):
    try:
        students = collection.find({"admin_id": current_admin["email"]})
        return all_students(students)
    except Exception as e:
        raise HTTPException(status_code=404, detail="An error occurred while fetching students")

# Get a specific student by student ID (only if it belongs to the logged-in admin)
@router.get("/get/{student_id}")
async def get_student(student_id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        student = collection.find_one({"student_id": student_id, "admin_id": current_admin["email"]})
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return individual_data(student)
    except Exception as e:
        raise HTTPException(status_code=404, detail="An error occurred while fetching the student")

# Get a specific student by MongoDB _id (only if it belongs to the logged-in admin)
@router.get("/get-by-mongodb-id/{mongodb_id}")
async def get_student_by_mongodb_id(mongodb_id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        student = collection.find_one({"_id": ObjectId(mongodb_id), "admin_id": current_admin["email"]})
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return individual_data(student)
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid MongoDB ID format")

# Update a specific student by student ID (only if it belongs to the logged-in admin)
@router.put("/update/{student_id}")
async def update_student(student_id: str, updated_student: Student, current_admin: dict = Depends(get_current_admin)):
    try:
        # Validate program and department compatibility
        validate_program_department(updated_student.program, updated_student.department)

        update_data = updated_student.dict(exclude_unset=True)
        result = collection.update_one(
            {"student_id": student_id, "admin_id": current_admin["email"]},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or no update made")
        return {"status_code": 200, "message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="An error occurred while updating the student")

# Delete a specific student by student ID (only if it belongs to the logged-in admin)
@router.delete("/delete/{student_id}")
async def delete_student(student_id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        result = collection.delete_one({"student_id": student_id, "admin_id": current_admin["email"]})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or not authorized to delete")
        return {"status_code": 200, "message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="An error occurred while deleting the student")

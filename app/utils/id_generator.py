from app.utils.config import collection, admin_collection

# Generate unique campus ID
def generate_campus_id():
    count = admin_collection.count_documents({})
    return str(count + 1).zfill(2)

# Function to generate student ID
def generate_student_id(campus_id: str):
    max_student_number = collection.count_documents({"student_id": {"$regex": f"^bc{campus_id}"}})
    student_number = max_student_number + 1
    student_id = f"bc{campus_id}{str(student_number).zfill(6)}"
    return student_id

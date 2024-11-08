from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from fastapi import HTTPException

# Predefined programs and their corresponding departments
PROGRAMS = {
    "BS English": "English Department",
    "BS Computer Science": "IT Department",
    "BS Business Administration": "Business Department",
    "BS Biology": "Science Department",
}

# Pydantic model for validating student data
class Student(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter Student Name")
    father_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter Father Name") 
    age: int = Field(..., ge=15, le=30, example=20)
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$", example="Enter 11 digit phone number")
    email: EmailStr = Field(..., example="Enter email like student@example.com") 
    address: str = Field(..., min_length=1, max_length=100, example="Enter Address")
    program: str = Field(..., example="Select Program")
    department: str = Field(..., example="Select Department")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 

    class Config:
        str_strip_whitespace = True

# Pydantic model for admin registration
class AdminRegistration(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter First Name")
    last_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s]+$", example="Enter Last Name")
    email: EmailStr = Field(..., example="Enter Admin Email")
    password: str = Field(..., min_length=8, max_length=128, example="Enter Password")
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$", example="Enter 11 digit phone number")
    campus: str = Field(..., example="Enter Campus Name")

    class Config:
        anystr_strip_whitespace = True  # Strip whitespace from strings

    # Validation for password strength
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise HTTPException(status_code=400, detail="Password must contain at least one numeral.")
        if not any(char.isupper() for char in password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")

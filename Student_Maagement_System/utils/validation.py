from fastapi import HTTPException
from Database.models import PROGRAMS

# Validate program and department compatibility
def validate_program_department(program: str, department: str):
    if PROGRAMS.get(program) != department:
        raise HTTPException(status_code=400, detail=f"The program '{program}' does not match the department '{department}'.")

# Validate admin registration
def validate_admin_registration(admin_data):
    # Check if admin email is valid
    if not admin_data.email or "@" not in admin_data.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate password strength
    if len(admin_data.password) < 8 or not any(char.isdigit() for char in admin_data.password) or not any(char.isupper() for char in admin_data.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long, contain at least one numeral and one uppercase letter.")

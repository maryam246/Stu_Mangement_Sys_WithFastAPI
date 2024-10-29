from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Database.models import AdminRegistration
from utils.config import admin_collection
from utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from utils.validation import validate_admin_registration
from utils.id_generator import generate_campus_id

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Admin registration endpoint
@router.post("/register")
async def register_admin(admin_data: AdminRegistration):
    # Validate admin registration
    validate_admin_registration(admin_data)

    # Check if admin already exists
    existing_admin_email = admin_collection.find_one({"email": admin_data.email})
    if existing_admin_email:
        raise HTTPException(status_code=400, detail="Admin email already registered")

    existing_admin_campus = admin_collection.find_one({"campus": admin_data.campus})
    if existing_admin_campus:
        raise HTTPException(status_code=400, detail="Campus already registered")

    # Register new admin
    hashed_password = hash_password(admin_data.password)
    campus_id = generate_campus_id()
    admin_collection.insert_one({
        "first_name": admin_data.first_name,
        "last_name": admin_data.last_name,
        "email": admin_data.email,
        "password": hashed_password,
        "phone": admin_data.phone,
        "campus": admin_data.campus,
        "campus_id": campus_id
    })

    return {"message": "Admin registered successfully", "campus_id": campus_id}

# Admin login endpoint to create token
@router.post("/login")
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate admin login using previously defined validation rules
    if not form_data.username or "@" not in form_data.username:
        raise HTTPException(status_code=400, detail="Invalid email format")

    admin = admin_collection.find_one({"email": form_data.username})
    if not admin or not verify_password(form_data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT token for the admin
    access_token = create_access_token(data={"sub": admin["email"]})
    return {
        "campus_name": admin["campus"],
        "campus_id": admin["campus_id"],
        "email": admin["email"],
        "access_token": access_token
    }

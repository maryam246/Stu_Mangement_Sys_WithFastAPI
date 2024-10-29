from fastapi import FastAPI
from routes.student import router as student_router  # Import the student router
from routes.admin import router as admin_router  # Import the admin router


app = FastAPI()

# Include the admin and student routers
app.include_router(admin_router, tags=["Admin"])
app.include_router(student_router, prefix="/students", tags=["Students"])

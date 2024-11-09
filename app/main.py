from fastapi import FastAPI
from app.routes.student import router as student_router  # Import the student router
from app.routes.admin import router as admin_router  # Import the admin router
import uvicorn
app = FastAPI()

# Include the admin and student routers
app.include_router(admin_router, tags=["Admin"])
app.include_router(student_router, prefix="/students", tags=["Students"])

# Entry point for running the app directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

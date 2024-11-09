# Student Management System
A simple Student Management System built with FastAPI and MongoDB for managing student data, including operations like creating, updating, deleting, and retrieving students' information. This system features schema validation with Pydantic and efficient database interactions using PyMongo.

## Features
- Create a new student with server-side generated student IDs.
- Retrieve student records by MongoDB Object ID or custom student ID.
- Update and delete student records by custom student ID.
- Input validation (e.g., age, phone number, email) using Pydantic models.
- Program and department validation to ensure consistency.
- MongoDB for data storage and retrieval.
- Automatic timestamps for created and updated records.
## Requirements
Before running the project, ensure you have the following installed by running this command:
```bash
pip install -r requirements.txt
```

## Installation
1. Clone the repository:

```bash
git clone https://github.com/maryam246/Student_Management_System.git
```

2. Navigate to the project directory:

```bash
cd Student_Maagement_System
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate
```
4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Create a .env file in the project root and add your MongoDB connection string and Your JWT secret key:

```bash
MONGODB_LINK=<your-mongodb-connection-string>
SECRET_KEY=<your-jwt-secret-key>
```

# Usage
1. Run the FastAPI application:

```bash
uvicorn main:app --reload
```

2. Open your browser and go to:
```bash
http://127.0.0.1:8000/docs
```
This will open the automatically generated Swagger UI, where you can interact with the API.

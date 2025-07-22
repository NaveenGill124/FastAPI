# =======================
# 📦 IMPORTING MODULES
# =======================

# Core FastAPI imports
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse

# Pydantic is used for data validation and serialization
from pydantic import BaseModel, Field, computed_field

# Type hinting and data annotation utilities
from typing import Annotated, Literal, Optional

# JSON module to handle reading/writing local data
import json

# =======================
# 🚀 FASTAPI INSTANCE
# =======================

app = FastAPI()  # This creates an instance of the FastAPI app


# ===========================
# 🧬 DATA MODEL USING PYDANTIC
# ===========================

# ▶️ Model for creating a Patient record
class Patient(BaseModel):
    # Patient ID - Required field
    id: Annotated[str, Field(..., description='ID of the Patient', example='P001')]
    
    # Name - Required
    name: Annotated[str, Field(..., description='Name of the Patient')]
    
    # City - Required
    city: Annotated[str, Field(..., description='City where the Patient is living')]
    
    # Age - Must be between 1 and 119
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the Patient')]
    
    # Gender - Must be 'male', 'female', or 'others'
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the Patient')]
    
    # Height in meters
    height: Annotated[float, Field(..., description='Height of the Patient in meters')]
    
    # Weight in kilograms
    weight: Annotated[float, Field(..., description='Weight of the Patient in kgs')]

    # Automatically compute BMI from height and weight
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Automatically return health verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"


# ▶️ Model for updating a Patient record (all fields optional)
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description='Name of the Patient')]
    city: Annotated[Optional[str], Field(default=None, description='City where the Patient is living')]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description='Age of the Patient')]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description='Gender of the Patient')]
    height: Annotated[Optional[float], Field(default=None, description='Height of the Patient in meters')]
    weight: Annotated[Optional[float], Field(default=None, description='Weight of the Patient in kgs')]


# ===========================
# 🗂️ FILE OPERATIONS FOR DATA
# ===========================

# Load existing data from JSON file
def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

# Save updated data back to JSON file
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


# ===========================
# 🔌 API ROUTES / ENDPOINTS
# ===========================

# 🌐 Root endpoint - just a welcome message
@app.get("/")
def hello():
    return {'message': 'Hello World'}

# 🧾 About the API
@app.get('/about')
def about():
    return {'message': 'Fully Functional API to Manage your Patient records'}

# 📋 View all patients
@app.get('/view')
def view():
    return load_data()


# 🔍 View a specific patient by ID
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient in DB", example='P001')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]

    # Return 404 error if patient not found
    raise HTTPException(status_code=404, detail='Patient not Found')


# 📊 Sort patients by height, weight, or BMI
@app.get('/sort')
def sort_patient(
    sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):
    valid_field = ['height', 'weight', 'bmi']

    # Validate sort field
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail='Invalid field. Select from height, weight, or bmi')

    # Validate order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Select between asc and desc')

    data = load_data()

    # Define sort direction
    sort_order = True if order == 'desc' else False

    # Perform sorting
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# ➕ Add a new patient record
@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    # Check for duplicate ID
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # Add new patient (excluding ID because it's already used as the key)
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


# ✏️ Update patient details
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_info = data[patient_id]

    # Only update fields that were passed in the request
    update_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    # Reconstruct the patient model to recalculate bmi and verdict
    existing_patient_info['id'] = patient_id  # Add ID to pass validation
    patient_pydantic_obj = Patient(**existing_patient_info)

    # Remove ID before saving back to JSON
    updated_patient_data = patient_pydantic_obj.model_dump(exclude=['id'])

    data[patient_id] = updated_patient_data

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})


# ❌ Delete a patient record
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient data not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})

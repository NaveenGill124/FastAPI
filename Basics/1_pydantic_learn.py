# ========================================
# 📦 Imports: Bring in Required Components
# ========================================

# BaseModel: The core class from Pydantic used for defining data models.
# EmailStr: A type that validates whether a string is a proper email format.
# AnyUrl: A type that validates whether a string is a valid URL.
# Field: Used to add constraints and metadata (e.g., max length, description).
from pydantic import BaseModel, EmailStr, AnyUrl, Field

# Typing tools:
# List[str] → A list that must contain strings
# Dict[str, str] → A dictionary where both keys and values are strings
# Optional → Marks a field as optional (i.e., can be None or missing)
# Annotated → Allows combining types with extra metadata or constraints
# Literal → Used to restrict a value to specific literal options (not used here but imported for reference)
from typing import List, Dict, Optional, Annotated, Literal


# ========================================
# 🧾 Patient Schema Definition (Pydantic Model)
# ========================================
# This model defines the structure of the data we expect for a patient.
# It enforces validation and helps generate interactive API docs (e.g., with FastAPI).

class Patient(BaseModel):

    # ========= Required Fields =========

    # A string field with a maximum length of 50 characters
    name: str = Field(max_length=50, description="Full name of the patient")

    # Automatically validates that the value is a valid email format
    email: EmailStr

    # Automatically validates that the value is a valid URL
    linkedin_url: AnyUrl

    # Surname with detailed metadata (title, description, examples)
    surname: Annotated[
        str,
        Field(
            max_length=20,
            title='Your Surname',
            description='Provide your surname (maximum 20 characters)',
            examples=['Gill', 'Singh']
        )
    ]

    # Age must be between 1 and 79 (both bounds exclusive)
    age: int = Field(gt=0, lt=80, description="Age must be between 1 and 79")

    # Weight must be a float greater than 0. `strict=True` ensures it's not a string like "72.5"
    weight: Annotated[float, Field(gt=0, strict=True)]

    # ========= Optional Fields =========

    # 'married' is an optional string field with description and example.
    # The `Optional` means it can be missing or set to None.
    # This currently expects a string like "Single", "Married", etc.
    married: Optional[Annotated[str, Field(description='Marital status', examples=['Married', 'Single', 'Divorced'])]] = None

    # A list of allergies. If provided, must be a list of strings.
    allergies: Optional[List[str]] = None

    # A dictionary with contact details, e.g., {'phone': '1234', 'emergency': '5678'}
    contact_details: Optional[Dict[str, str]] = None


# ========================================
# 📥 Simulated Data Insertion Function
# ========================================
# This function simulates storing or processing the patient record (like a POST endpoint in FastAPI)

def insert_patient_data(patient: Patient):
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age}")
    print("Patient record inserted successfully.")


# ========================================
# 📦 Input Dictionary for Testing the Model
# ========================================
# Here we simulate incoming data as a dictionary. This could come from a frontend form or API request.

Patient_info = {
    'name': 'Naveen',                       # Valid name (string, ≤50 chars)
    'surname': 'Gill',                      # Valid surname (string, ≤20 chars)
    'email': 'gill@gmail.com',              # Valid email
    'linkedin_url': 'http://linkedin.com/naveen',  # Valid URL
    'age': 20,                              # Valid age (between 1 and 79)
    'weight': 76.3,                         # Valid weight (> 0)
    'married': 'Single',                    # Optional marital status (valid string)
    'allergies': ['pollen', 'dust']         # Optional list of allergies
    # 'contact_details' is optional and not provided here
}


# ========================================
# 🛠️ Create the Patient Object and Insert It
# ========================================
# This creates a Patient instance from the dictionary.
# Pydantic will automatically validate all fields according to the constraints.

Patient1 = Patient(**Patient_info)

# Simulate inserting the patient record (could be a DB save in real apps)
insert_patient_data(Patient1)

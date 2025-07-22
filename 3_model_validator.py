# What we are going to test is: if age > 60 then emergency contact number should be there...

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl

    age: int
    weight: float

    married: Optional[Annotated[bool, Field(description='Married status', examples=[True, False])]] = None
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    
    
    @model_validator(mode = 'after')
    def validate_emergency_contact(cls, model):
        
        if model.age> 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact")
        
        return model
    
    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("updated")

Patient_info = {
    'name': 'Naveen Gill',
    'email': 'gill@hdfc.com',  # ✅ Valid domain
    'linkedin_url': 'http://linkedin.com/in/naveen',
    'age': '20',
    'weight': 76.3,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {  # ✅ Required field
        'phone': '9876543210',
        'emergency': '112'
    }
}

Patient1 = Patient(**Patient_info)
insert_patient_data(Patient1)
# What we are going to test is: if age > 60 then emergency contact number should be there...

from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated
import select

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl

    age: int
    weight: float # kgs
    height: float #mts

    married: Optional[Annotated[bool, Field(description='Married status', examples=[True, False])]] = None
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    
    
    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2) # round of upto two decimals
        return bmi 
        
    
    

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI', patient.calculate_bmi) # when we create a computed field then it will become
    print("updated")

Patient_info = {
    'name': 'Naveen Gill',
    'email': 'gill@hdfc.com',  # ✅ Valid domain
    'linkedin_url': 'http://linkedin.com/in/naveen',
    'age': '20',
    'weight': 76.3,
    'height' : 1.5,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {  # ✅ Required field
        'phone': '9876543210',
        'emergency': '112'
    }
}

Patient1 = Patient(**Patient_info)
update_patient_data(Patient1)
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator 
from typing import List, Dict, Optional, Annotated
# we are checking is there .sbi.com, @hdfc.com is in the email or not
class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl

    #surname: Optional[Annotated[str, Field(max_length=20, title='Your Surname', description='Give max of 20 length', examples=['Gill', 'Singh'])]]
    age: int
    weight: float

    married: Optional[Annotated[bool, Field(description='Married status', examples=[True, False])]] = None
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]
    
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        
        valid_domain = ['hdfc.com', 'sbi.com']
        #abc@gmail.com
        
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domain:
            raise ValueError('not a valid domain')
        
        return value
    
    @field_validator('name')
    @classmethod
    def transfor_text(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        
        if 0< value < 100:
            return value
        else:
            raise ValueError('Age Should be greator then 0 and less then 100')


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
    'age': '24',
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
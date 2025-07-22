#leys try to export this model into dict and json

from pydantic import BaseModel


class Address(BaseModel):
    
    city: str
    state: str
    
    pincode: str
    
class Patient(BaseModel):
    
    
    name: str
    gender: str
    age: int
    address: Address


address_dict = {'city': 'hisar', 'state' : 'haryana', 'pincode': '125033'}

address1 = Address(**address_dict)

patient_dict = {'name' : 'Naveen Gill', 'gender' : 'male', 'age': '25', 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump()

print(temp)

print(type(temp))

temp1 = patient1.model_dump_json()

print(temp1)

print(type(temp1))

temp3 = patient1.model_dump(include='name') 
# include means we only want these and also there is a oprtion, if we want to exclude
# there is one parameter which is exclude_unset, explain with above example


print(temp3)

print(type(temp3))
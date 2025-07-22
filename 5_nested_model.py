from pydantic import BaseModel


class Address(BaseModel):
    
    city: str
    state: str
    
    pincode: str
    
class Patient(BaseModel):
    
    
    name: str
    gender: str
    age: int
    # adress can be made using different datatypes and sometime we need pincode, state city diffrently so we nee to make another model that we can use as a field in it
    address: Address


address_dict = {'city': 'hisar', 'state' : 'haryana', 'pincode': '125033'}

address1 = Address(**address_dict)

patient_dict = {'name' : 'Naveen Gill', 'gender' : 'male', 'age': '25', 'address': address1}

patient1 = Patient(**patient_dict)

print(patient1)
# now we can check anything like

print(patient1.name)
print(patient1.address.city)
print(patient1.address.pincode)
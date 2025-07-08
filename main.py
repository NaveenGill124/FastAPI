from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()

# let's create a function which will load the data from the json file

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f) 
    return data 

    

@app.get("/")

def hello():
    return {'message': 'Hello World'}

@app.get('/about')

def about():
    
    return {'message': 'Fully Functional API to Manage your Patient records'}

@app.get('/view')

def view():
    
    return load_data()


@app.get('/patient/{patient_id}')

def view_patient(patient_id: str = Path(..., description= "ID of the patient in DB", example='P001')): # our id is string because in patients.json file id is string
    
    # first we will load the patient data
    
    data = load_data()
    
    if patient_id in data:
        
        return data[patient_id]

    # return {'ERROR' : 'patient is not found...'} 
    # this is not the right way because what we are doing is simply return json content with 200 HTTP state code
    # we need to show 404 code if data not found that's why we'll use HTTPException
    
    raise HTTPException(status_code = 404, detail ='Patient not Found')
    
    

@app.get('/sort')

def sort_patient(sort_by: str = Query(..., description='Sort on the basis of heigh, weight or bmi'), order : str = Query('asc', description='sort in asc pr desc order...')):
    
    valid_field = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f'Invalifd field select from')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail = 'Invalid order select betwenn asc and desc')

    data = load_data()
    
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get('sort_by', 0), reverse=sort_order)
    return sorted_data
    
    
    

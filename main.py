from typing import Optional

from fastapi import FastAPI

emp=[
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Smith"}
]

app = FastAPI()

@app.get("/display") 
def read_root():
    return {"Hello": "World"}

#output: http://host:8000/display

# path parameters
@app.get("/display/{id}")
def read_item(id: int):
    for employee in emp:
        if employee["id"] == id:
            return employee
    return {"error": "Employee not found"}

#output: http://host:8000/display/1


# query parameters
@app.get("/display/query")
def read_query(id: int):
    for employee in emp:
            if employee["id"] == id:
                return employee
            return {"error": "Employee not found"}

#output: http://host:8000/display/query?id=1

#Request body
#   used to send structured data to the server. In FastAPI, you can define a request body using Pydantic models.

#pydantic model
# 1) validation is used to validate the data sent in the request body. FastAPI automatically validates the data based on the Pydantic model you define.
# 2) serialization is used to convert the data from the request body into Python objects that can be easily manipulated in your code. FastAPI automatically serializes the data based on the Pydantic model you define.
# 3) documentation is used to generate API documentation based on the Pydantic model you define. FastAPI automatically generates documentation for your API endpoints based on the request body and response models you define.

from pydantic import BaseModel, Field
from typing import Optional


#nested model

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Employee(BaseModel):
     name: str = Field(min_length=3, max_length=50, pattern="^[a-zA-Z]+$") 
     price: float = Field(gt=0, description="Price must be greater than zero")
     available: Optional[bool] = None
     address: Address

@app.post("/display")
def create_employee(data : Employee):
    return {"message": "Employee created successfully", "data": data}


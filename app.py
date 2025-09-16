from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()
# 1. Define the blueprint for APIs
class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

# 2. Create the API Endpoint
## Database for Now:
customer_list = []

## Create - POST
@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    customer_list.append(customer)
    return customer

## Read - GET
@app.get("/customers", response_model=List[Customer])
def get_customers():
    return customer_list

## UPDATE - PUT
@app.put("/customers/{id}", response_model=Customer)
def update_customer(id: int, customer: Customer):
    for i, existing_customer in enumerate(customer_list):
        if existing_customer.id == id:
            customer_list[i] = customer
            return customer
    raise HTTPException(status_code=404, detail="Customer Not Found")

    
## Delete - DELETE
@app.delete("/customers/{id}", response_model=Customer)
def delete_customer(id: int):
    for i, existing_customer in enumerate(customer_list):
        if existing_customer.id == id:
            deleted_customer = customer_list.pop(i)
            return deleted_customer
    raise HTTPException(status_code=404, detail="Customer Not Found")

# Running on Public URL
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
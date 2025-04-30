from models.Warehouse import Warehouses
from database import sesiune as db
from pydantic import BaseModel
from api.app import getApp
from fastapi import HTTPException
app = getApp()

@app.get("/api/warehouses")
async def list_warehouses(page: int = 1, page_size: int = 10):
    sesiune = db.getSession()
    warehouses = (
        sesiune.query(Warehouses)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    result = [
        {
            "id": warehouse.id,
            "name": warehouse.name,
            "location": warehouse.location
        }
        for warehouse in warehouses
    ]

    return result
class CreateWarehouse(BaseModel):
    name: str
    location: str

@app.post("/api/warehouses")
async def create_warehouse(request: CreateWarehouse):
    sesiune = db.getSession()
    if not request.name or not request.location:
        raise HTTPException(status_code=400, detail="Name and location must not be empty.")
    
    existing = sesiune.query(Warehouses).filter_by(name=request.name, location=request.location).first()
    if existing:
        raise HTTPException(status_code=409, detail="Warehouse already exists.")
    
    warehouse = Warehouses(
        name=request.name,
        location =request.location,
    )
    
    sesiune.add(warehouse)
    sesiune.commit()
    sesiune.refresh(warehouse)

    return{"message": "Warehouse created successfully", "id": warehouse.id}


@app.get("/api/warehouses/{warehouse_id}")
async def get_warehouse(warehouse_id: str):
    sesiune = db.getSession()
    warehouse = sesiune.query(Warehouses).filter_by(id=warehouse_id).first()

    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found.")

    return {
        "id": warehouse.id,
        "name": warehouse.name,
        "location": warehouse.location
    }
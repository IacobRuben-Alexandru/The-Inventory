from decimal import Decimal
from uuid import uuid4
from models.Warehouse import Warehouses
from models.Supplier import Suppliers
from models.Product import Products
from database import sesiune as db
from pydantic import BaseModel, Extra
from api.app import getApp
from fastapi import Body, HTTPException
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

class UpdateWarehouse(BaseModel):
    location: str = None


@app.patch("/api/warehouses/{warehouse_id}")
async def update_warehouse(warehouse_id: str, request: UpdateWarehouse):
    sesiune = db.getSession()
    warehouse = sesiune.query(Warehouses).filter_by(id=warehouse_id).first()

    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found.")

    if request.location:
        warehouse.location = request.location

    sesiune.commit()
    sesiune.refresh(warehouse)

    return {
        "message": "Warehouse updated successfully"
    }

@app.put("/api/warehouses/{warehouse_id}")
async def update_or_create_warehouse(warehouse_id: str, request: CreateWarehouse):
    sesiune = db.getSession()

    duplicate_warehouse = sesiune.query(Warehouses).filter(
        Warehouses.name == request.name,
        Warehouses.location == request.location,
        Warehouses.id != warehouse_id
    ).first()

    if duplicate_warehouse:
        raise HTTPException(
            status_code=409,
            detail="A warehouse with the same name and location already exists."
        )

    warehouse = sesiune.query(Warehouses).filter_by(id=warehouse_id).first()

    if warehouse:
        if warehouse.name != request.name and warehouse.location != request.location:
            new_warehouse = Warehouses(
                id=str(uuid4()),
                name=request.name,
                location=request.location
            )
            sesiune.add(new_warehouse)
            sesiune.commit()
            sesiune.refresh(new_warehouse)

            return {"message": "Warehouse created successfully"}

        if warehouse.name != request.name or warehouse.location != request.location:
            warehouse.name = request.name
            warehouse.location = request.location

        sesiune.commit()
        sesiune.refresh(warehouse)

        return {"message": "Warehouse updated successfully"}

    # new_warehouse = Warehouses(
    #     id=warehouse_id,
    #     name=request.name,
    #     location=request.location
    # )
    # sesiune.add(new_warehouse)
    # sesiune.commit()
    # sesiune.refresh(new_warehouse)

    # return {"message": "Warehouse created successfully"}

class CreateSupplier(BaseModel):
    name: str
    contactEmail: str


@app.post("/api/suppliers")
async def create_supplier(request: CreateSupplier):
    sesiune = db.getSession()
    if not request.name or not request.contactEmail:
        raise HTTPException(status_code=400, detail="Name and email must not be empty.")
    
    existing = sesiune.query(Suppliers).filter_by(name=request.name, contactEmail=request.contactEmail).first()
    if existing:
        raise HTTPException(status_code=409, detail="Supplier already exists.")
    
    suppliers = Suppliers(
        name=request.name,
        contactEmail =request.contactEmail,
    )
    
    sesiune.add(suppliers)
    sesiune.commit()
    sesiune.refresh(suppliers)

    return{"message": "Supplier created successfully", "id": suppliers.id}

@app.get("/api/suppliers")
async def AllSuppliers(page: int = 1, page_size: int = 10):
    sesiune = db.getSession()
    suppliers = (
        sesiune.query(Suppliers)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    result = [
        {
            "id": supplier.id,
            "name": supplier.name,
            "contactEmail": supplier.contactEmail
        }
        for supplier in suppliers
    ]

    return result

@app.get("/api/suppliers/{supplier_id}")
async def get_supplier(supplier_id: str):
    sesiune = db.getSession()
    supplier = sesiune.query(Suppliers).filter_by(id=supplier_id).first()

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")

    return {
        "id": supplier.id,
        "name": supplier.name,
        "contactEmail": supplier.contactEmail
    }

class UpdateSupplier(BaseModel):
    contactEmail: str = None

@app.patch("/api/suppliers/{supplier_id}")
async def update_supplier(supplier_id: str, request: UpdateSupplier):
    sesiune = db.getSession()
    supplier = sesiune.query(Suppliers).filter_by(id=supplier_id).first()

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")

    if request.contactEmail:
        supplier.contactEmail = request.contactEmail

    sesiune.commit()
    sesiune.refresh(supplier)

    return {
        "message": "Supplier updated successfully"
    }

@app.put("/api/suppliers/{supplier_id}")
async def update_or_create_supplier(supplier_id: str, request: CreateSupplier):
    sesiune = db.getSession()

    duplicate_supplier = sesiune.query(Suppliers).filter(
        Suppliers.name == request.name,
        Suppliers.contactEmail == request.contactEmail,
        # Suppliers.id != supplier_id
    ).first()

    if duplicate_supplier:
        raise HTTPException(
            status_code=409,
            detail="A supplier with the same name and contact email already exists."
        )

    supplier = sesiune.query(Suppliers).filter_by(id=supplier_id).first()

    if supplier:
        if supplier.name != request.name and supplier.contactEmail != request.contactEmail:
            new_supplier = Suppliers(
                id=str(uuid4()),  
                name=request.name,
                contactEmail=request.contactEmail
            )
            sesiune.add(new_supplier)
            sesiune.commit()
            sesiune.refresh(new_supplier)

            return {"message": "Supplier created successfully"}
        if supplier.name != request.name or supplier.contactEmail != request.contactEmail:
            supplier.name = request.name
        sesiune.commit()
        sesiune.refresh(supplier)

        return {"message": "Supplier updated successfully"}

class CreateProduct(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str
    stockQuantity: int

@app.post("/api/warehouses/{warehouseId}/products")
async def create_product(warehouseId: str, request: CreateProduct):
    sesiune = db.getSession()
    if not request.name or not request.description or not request.price or not request.category or not request.stockQuantity:
        raise HTTPException(status_code=400, detail="Nothing should be empty.")
    
    existing = sesiune.query(Products).filter_by(name=request.name, description=request.description, price=request.price, category=request.category, stockQuantity=request.stockQuantity,warehouseId = warehouseId).first()
    if existing:
        raise HTTPException(status_code=409, detail="Product already exists.")
    
    product = Products(
        name=request.name,
        description =request.description,
        price =request.price,
        category =request.category,
        stockQuantity =request.stockQuantity,
        warehouseId = warehouseId,
    )
    
    sesiune.add(product)
    sesiune.commit()
    sesiune.refresh(product)

    return{"message": "Product created successfully", "id": product.id}

@app.get("/api/warehouses/{warehouseId}/products")
async def AllProducts(warehouseId: str, page: int = 1, page_size: int = 10):
    sesiune = db.getSession()
    products = (
        sesiune.query(Products)
        .filter_by(warehouseId=warehouseId)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    result = [
        {
            "id": product.id,
            "name": product.name,
            "sku": product.sku,
            "price": product.price,
            "stockQuantity": product.stockQuantity
        }
        for product in products
    ]

    return result

@app.get("/api/warehouses/{warehouseId}/products/{product_id}")
async def get_product(warehouseId: str, product_id: str):
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "sku": product.sku,
        "price": product.price,
        "category": product.category,
        "stockQuantity": product.stockQuantity
    }

class UpdateProduct(BaseModel, extra=Extra.allow):
    price: Decimal | None = None
    name: str | None = None
    description: str | None = None
    

@app.patch("/api/warehouses/{warehouseId}/products/{product_id}")
async def update_product(warehouseId: str, product_id: str, request: dict = Body(...)):
    if "stockQuantity" in request:
        raise HTTPException(status_code=400, detail="Stock quantity cannot be updated via this endpoint.")
    
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    for key, value in request.items():
        if hasattr(product, key):
            setattr(product, key, value)

    sesiune.commit()
    sesiune.refresh(product)

    return {"message": "Product updated successfully"}

class ProductUpdateOrCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str
    stockQuantity: int

@app.put("/api/warehouses/{warehouseId}/products/{product_id}")
async def put_product(warehouseId: str, product_id: str, request: ProductUpdateOrCreate):
    sesiune = db.getSession()

    existing_product = sesiune.query(Products).filter(
        Products.name == request.name,
        # Products.price == request.price,
        # Products.description == request.description,
        Products.category == request.category,
        Products.warehouseId == warehouseId
    ).first()

    if existing_product:
        if existing_product.id != product_id:
            raise HTTPException(
                status_code=409,
                detail="A product with the same name, price, description, and category already exists in the warehouse."
            )

        if existing_product.stockQuantity != request.stockQuantity:
            raise HTTPException(
                status_code=400,
                detail="Stock quantity cannot be updated via this endpoint. Please use the Stock Management endpoint."
            )

        existing_product.name = request.name
        existing_product.description = request.description
        existing_product.price = request.price
        existing_product.category = request.category

        sesiune.commit()
        sesiune.refresh(existing_product)

        return {"message": "Product updated successfully", "sku": existing_product.sku}

    new_product = Products(
        id=str(uuid4()),
        warehouseId=warehouseId,
        name=request.name,
        description=request.description,
        price=request.price,
        category=request.category,
        stockQuantity=request.stockQuantity
    )
    sesiune.add(new_product)
    sesiune.commit()
    sesiune.refresh(new_product)

    return {"message": "Product created successfully", "sku": new_product.sku}




@app.delete("/api/warehouses/{warehouseId}/products/{product_id}")
async def delete_product(warehouseId: str, product_id: str):
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    sesiune.delete(product)
    sesiune.commit()

    return {"message": "Product deleted successfully"}

#Stock Management
@app.get("/api/warehouses/{warehouseId}/inventory")
async def get_stock_all(warehouseId: str, page: int = 1, page_size: int = 10):
    sesiune = db.getSession()
    products = (
        sesiune.query(Products)
        .filter_by(warehouseId=warehouseId)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    result = [
        {
            "id": product.id,
            "sku": product.sku,
            "stockQuantity": product.stockQuantity
        }
        for product in products
    ]

    return result

@app.get("/api/warehouses/{warehouseId}/inventory/{product_id}")
async def get_stock(warehouseId: str, product_id: str):
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return {
        "id": product.id,
        "sku": product.sku,
        "stockQuantity": product.stockQuantity
    }

class IncreaseStockRequest(BaseModel):
    quantity: int
    supplierId: str

@app.post("/api/warehouses/{warehouseId}/inventory/{product_id}/increase")
async def increase_stock(
    warehouseId: str,
    product_id: str,
    payload: IncreaseStockRequest,
):
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    supplier = sesiune.query(Suppliers).filter_by(id=payload.supplierId).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")

    if hasattr(product, "supplierId") and product.supplierId != payload.supplierId:
        raise HTTPException(
            status_code=400,
            detail=f"Product is not associated with supplier {payload.supplierId}"
        )

    product.stockQuantity += payload.quantity
    sesiune.commit()
    sesiune.refresh(product)

    return {
        "message": "Stock increased successfully",
        "newStockQuantity": product.stockQuantity
    }

class DecreaseStockRequest(BaseModel):
    quantity: int
    reason: str

@app.post("/api/warehouses/{warehouseId}/inventory/{product_id}/decrease")
async def increase_stock(
    warehouseId: str,
    product_id: str,
    payload: DecreaseStockRequest,
):
    sesiune = db.getSession()
    product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")


    product.stockQuantity -= payload.quantity
    sesiune.commit()
    sesiune.refresh(product)

    return {
        "message": "Stock decreased successfully",
        "newStockQuantity": product.stockQuantity
    }

class TransferStockRequest(BaseModel):
    quantity: int
    targetWarehouseId: str
    reason: str
@app.post("/api/warehouses/{warehouseId}/inventory/{product_id}/transfer")
async def transfer_stock(
    warehouseId: str,
    product_id: str,
    payload: TransferStockRequest,  
):
    sesiune = db.getSession()
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")

    source_product = sesiune.query(Products).filter_by(id=product_id, warehouseId=warehouseId).first()
    if not source_product:
        raise HTTPException(status_code=404, detail="Source product not found.")

    if source_product.stockQuantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock in source warehouse.")

    target_product = sesiune.query(Products).filter_by(id=product_id, warehouseId=payload.targetWarehouseId).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="Product not found in destination warehouse.")

    source_product.stockQuantity -= payload.quantity
    target_product.stockQuantity += payload.quantity

    sesiune.commit()
    sesiune.refresh(source_product)
    sesiune.refresh(target_product)

    return {
        "message": "Stock transferred successfully",
        "newStockQuantity": target_product.stockQuantity
    }
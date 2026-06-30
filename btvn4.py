from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str
    name: str
    price: int
    stock: int

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    product_found = False
    current_product = None
    for item in products:
        if item["id"] == product_id:
            product_found = True
            current_product = item
            break

    if not product_found:
        raise HTTPException(status_code=404, detail="Product not found")
    for item in products:
        if item["code"] == product.code and item["id"] != product_id:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )
    if product.name == "":
        raise HTTPException(status_code=400, detail="Product name cannot be empty")

    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    if product.stock < 0:
        raise HTTPException(status_code=400, detail="Stock must be greater than or equal to 0")

    # Cập nhật thông tin
    current_product["code"] = product.code
    current_product["name"] = product.name
    current_product["price"] = product.price
    current_product["stock"] = product.stock

    return current_product
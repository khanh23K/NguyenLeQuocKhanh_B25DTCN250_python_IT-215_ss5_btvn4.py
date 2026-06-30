from fastapi import FastAPI
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
    index = -1

    for i in range(len(products)):
        if products[i]["id"] == product_id:
            product_found = True
            index = i
            break

    if product_found == False:
        return {"detail": "Product not found"}

    for item in products:
        if item["code"] == product.code and item["id"] != product_id:
            return {"detail": "Product code already exists"}

    if product.name == "":
        return {"detail": "Product name cannot be empty"}

    if product.price <= 0:
        return {"detail": "Price must be greater than 0"}

    if product.stock < 0:
        return {"detail": "Stock must be greater than or equal to 0"}

    products[index]["code"] = product.code
    products[index]["name"] = product.name
    products[index]["price"] = product.price
    products[index]["stock"] = product.stock

    return products[index]
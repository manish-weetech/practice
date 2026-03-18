from fastapi import FastAPI, Request
from mockData import products
from dtos import ProductDTO

app = FastAPI()

@app.get("/")
def home():
    return "welcome"

@app.get("/products")
def get_products():
    return products

#path param
@app.get("/product/{id}")
def get_one_product(id:int):
    
    for i in products:
        if i.get("id") == id:
            return i

    return {
        "error": "product not found"
    }

# query params
# @app.get("/greet")
# def greet_user(name:str, age:int):
#     return {
#         "greet": f"Hello {name}! your age is {age}"
#     }

@app.get("/greet")
def greet_user(request: Request):
    query_params = dict(request.query_params)
    print(query_params)
    return {
        "greet": f"Hello {query_params.get("name")}! your age is {query_params.get("age")}"
    }

# different type of http methods
# how to validate data - DTOS
# How to call different HTTP Methods - Any TOOL

@app.post("/create_product")
def create_product(body: ProductDTO):
    product_data = body.model_dump()
    products.append(product_data)

    return {"status":"Created","data":products}

# pydantic

@app.put("/update_product/{product_id}")
def update_product(product_data: ProductDTO, product_id:int):
    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == product_id:
            products[index] = product_data.model_dump()
            return {"status":"updated", "product": product_data}

    return {
        "error": "product not found"
    }

@app.delete("/delete_product/{product_id}")
def delete_product(product_id:int):
    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == product_id:
            delete_product = products.pop(index)
            return {"status":"Deleted", "product": delete_product}

    return {
        "error": "product not found"
    }


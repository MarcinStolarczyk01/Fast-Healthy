from fastapi import FastAPI

app = FastAPI()

# TODO: DB should have 2 tables: products & recipes
# TODO: products should have properties: name,
# TODO: Add option for displaying products
@app.get('/')
def get_route():
    return 'Welcome to Fast&Healthy, tool that makes diet easy!'

@app.get('/products')
def get_products():
    return
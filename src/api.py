from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to Fast&Healthy API!"


@app.get("/recipes")
def get_recipes():
    raise NotImplemented


@app.post("/recipes")
def post_recipes(recipe):
    raise NotImplemented


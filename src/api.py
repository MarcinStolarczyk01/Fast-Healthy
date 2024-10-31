from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to Fast&Healthy API!"


@app.get("/recipes")
def get_recipes():
    pass


@app.post("/recipes")
def post_recipes(recipe):
    pass

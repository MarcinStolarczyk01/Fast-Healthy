from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from src.dietitian.dietitian import Dietitian
from src.models.recipe.recipe import RecipeModel

app = FastAPI()
dietitian = Dietitian()


@app.get("/")
def root():
    return "Welcome to Fast&Healthy API!"


@app.get("/recipes", status_code=200)
def get_recipes():
    raise NotImplemented


@app.post("/recipes", status_code=201)
def post_recipes(recipe: dict):
    try:
        dietitian.add_recipe(RecipeModel(**recipe))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"ValidationError: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {e}")


@app.post("/config", status_code=201)
def configure_dietitian():
    raise NotImplemented

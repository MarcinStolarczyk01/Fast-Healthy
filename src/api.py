from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from src.dietitian.dietitian import Dietitian
from src.models.recipe.recipe import RecipeModel

app = FastAPI()
dietitian = Dietitian()


@app.get("/")
def root():
    return "Welcome to Fast&Healthy API!"


@app.get("/recipes", status_code=HTTPStatus.OK)
def get_recipes():
    try:
        return dietitian.get_recipes().model_dump_json()
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )


@app.post("/recipes", status_code=HTTPStatus.CREATED)
def post_recipes(recipe: dict):
    try:
        dietitian.add_recipe(RecipeModel(**recipe))
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"ValidationError: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )


@app.post("/config", status_code=201)
def configure_dietitian():
    raise NotImplemented

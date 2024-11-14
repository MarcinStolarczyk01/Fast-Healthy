import json
from http import HTTPStatus
from typing import Union, Literal

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel

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


class DeleteRecipesModel(BaseModel):
    recipes: Union[list[str], Literal["*"]]


@app.post("/recipes/delete", status_code=HTTPStatus.OK)
def del_recipes(delete_request: dict):
    try:
        dietitian.del_recipes(DeleteRecipesModel(**delete_request))
        return json.dumps({"message": "Successfully deleted recipes"})
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

import json
from http import HTTPStatus
from typing import Union, Literal

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel

from src.dietitian.dietitian import MacrosRatio
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
        return json.loads(dietitian.get_recipes().model_dump_json())
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )


@app.post("/recipes", status_code=HTTPStatus.CREATED)
def post_recipes(recipe: RecipeModel):
    try:
        dietitian.add_recipe(recipe)
        return {"message": "Successfully added the recipe"}
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
def del_recipes(delete_request: DeleteRecipesModel):
    try:
        dietitian.del_recipes(delete_request)
        return {"message": "Successfully deleted recipes"}
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"ValidationError: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )


class ConfigModel(BaseModel):
    kcal_goal: int
    meals_num: int
    macros_ratio: MacrosRatio


@app.post("/config", status_code=HTTPStatus.OK)
def configure_dietitian(config: ConfigModel):
    try:
        dietitian.kcal_goal(config.kcal_goal).meals_num(config.meals_num).macros_ratio(
            config.macros_ratio
        )
        return {"message": "Configured successfully"}
    except (ValidationError, ValueError) as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"ValidationError: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )

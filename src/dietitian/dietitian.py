from __future__ import annotations
from pydantic import BaseModel, model_validator
import numpy as np

from src.files_io_manager.files_io_manager import FilesIOManager, RecipesJsonModel
from src.models.recipe.recipe import Recipe, RecipeModel


class MacrosRatio(BaseModel):
    """Macro ingredients percentage content <0.0, 1.0>"""

    protein: float
    fat: float
    carbohydrates: float

    # Configuration for immutability
    model_config = {"frozen": True}

    @model_validator(mode="after")
    def __post_init__(self):
        if not all(
                [
                    np.isclose(self.protein + self.fat + self.carbohydrates, 1, atol=0.01),
                    self.protein >= 0,
                    self.fat >= 0,
                    self.carbohydrates >= 0,
                ]
        ):
            raise ValueError(
                f"""Macros coefficients must sum to one. Current macros coefficients: protein : {self.protein}
                                                                                     fat : {self.fat}
                                                                                     carbohydrates : {self.carbohydrates}"""
            )  # todo: custom exception like BadMacrosContentError
        return self


class Dietitian:
    """Class implementing fluent interface pattern"""

    def __init__(self):
        self._kcal_goal: int | None = 2000
        self._meals_num: int | None = 4
        self._macros_ratio: MacrosRatio = MacrosRatio(
            protein=0.25, fat=0.30, carbohydrates=0.45
        )

    def kcal_goal(self, kcal_goal: int) -> Dietitian:
        if not 1000 < kcal_goal < 5000:
            raise ValueError(
                f"kcal_goal={kcal_goal} out of range, it should be in <1000, 5000>"
            )  # todo: custom exception like KcalOutOfRange
        self._kcal_goal = kcal_goal
        return self

    def meals_num(self, meals_num: int) -> Dietitian:
        if not 1 < meals_num < 6:
            raise ValueError(
                f"meals_num={meals_num} out of range, it should be in <1, 6>"
            )  # todo: custom exception like MealsNumberOutOfRange
        self._meals_num = meals_num
        return self

    def macros_ratio(self, macros_content: MacrosRatio) -> Dietitian:
        self._macros_ratio = macros_content
        return self

    def add_recipe(self, post_recipe: RecipeModel) -> Dietitian:
        FilesIOManager.add_recipe(post_recipe)
        return self

    @staticmethod
    def get_recipes() -> RecipesJsonModel:
        return FilesIOManager.get_recipes()

    def get_diet(self) -> None:  # pd.DataFrame:
        raise NotImplementedError

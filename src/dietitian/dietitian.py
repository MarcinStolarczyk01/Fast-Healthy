from __future__ import annotations
from pydantic import BaseModel
import numpy as np
import pandas as pd



class MacrosContent(BaseModel):
    """Macro ingredients percentage content <0.0, 1.0>"""
    protein: float
    fat: float
    carbohydrates: float

    def __post_init__(self):
        if not all([np.isclose(self.protein + self.fat + self.carbohydrates, 1, atol=0.01),
                    self.protein >= 0,
                    self.fat >= 0,
                    self.carbohydrates >= 0]):
            raise ValueError()  # todo: custom exception like BadMacrosContentError


class Dietitian:
    """ Class implementing fluent interface pattern"""
    def __init__(self):
        self._kcal_goal: int | None = None
        self._meals_num: int | None = None
        self._macros_content : MacrosContent = MacrosContent(protein=0.25, fat=0.30, carbohydrates=0.45)

    def kcal_goal(self, kcal_goal: int) -> Dietitian:
        if not 1000 < kcal_goal < 5000:
            raise ValueError()  # todo: custom exception like KcalOutOfRange
        self._kcal_goal = kcal_goal
        return self

    def meals_num(self, meals_num: int) -> Dietitian:
        if not 1 < meals_num < 6:
            raise ValueError()  # todo: custom exception like MealsNumberOutOfRange
        self._meals_num = meals_num
        return self

    def macros_content(self, macros_content: MacrosContent) -> Dietitian:
        self._macros_content = macros_content
        return self

    def get_diet(self) -> pd.DataFrame:
        raise NotImplementedError()
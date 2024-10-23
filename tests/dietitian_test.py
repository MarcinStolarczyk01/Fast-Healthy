import pytest

from src.dietitian.dietitian import Dietitian
from src.dietitian.dietitian import MacrosRatio


@pytest.mark.parametrize(
    "kcal_goal, meals_num, macros_ratio",
    [(1100, 3, MacrosRatio(protein=0.3, fat=0.3, carbohydrates=0.4))],
)
def test_dietitian_fluent_pattern(kcal_goal, meals_num, macros_ratio) -> None:
    dietitian = (
        Dietitian().kcal_goal(kcal_goal).meals_num(meals_num).macros_ratio(macros_ratio)
    )
    assert dietitian._kcal_goal == kcal_goal
    assert dietitian._meals_num == meals_num
    assert dietitian._macros_ratio == macros_ratio


@pytest.mark.parametrize(
    "kcal_goal, meals_num, macros_ratio, expected_error",
    [
        (
            8000,
            3,
            MacrosRatio(protein=0.3, fat=0.3, carbohydrates=0.4),
            ValueError("kcal_goal=8000 out of range, it should be in <1000, 5000>"),
        ),
        (
            3000,
            10,
            MacrosRatio(protein=0.3, fat=0.3, carbohydrates=0.4),
            ValueError("meals_num=10 out of range, it should be in <1, 6>"),
        ),
    ],
)
def test_dietitian_raise_error(
    kcal_goal, meals_num, macros_ratio, expected_error
) -> None:
    with pytest.raises(type(expected_error), match=str(expected_error)):
        Dietitian().kcal_goal(kcal_goal).meals_num(meals_num).macros_ratio(macros_ratio)


@pytest.mark.parametrize(
    "protein, fat, carbohydrates, expected_error",
    [
        (
            0.5,
            0.5,
            0.2,
            ValueError(
                """Macros coefficients must sum to one. Current macros coefficients: protein : 0.5
                                                                                      fat : 0.5
                                                                                      carbohydrates : 0.2"""
            ),
        )
    ],
)
def test_macros_ratio_return_error(protein, fat, carbohydrates, expected_error) -> None:
    with pytest.raises(type(expected_error), match=str(expected_error)):
        MacrosRatio(protein=protein, fat=fat, carbohydrates=carbohydrates)

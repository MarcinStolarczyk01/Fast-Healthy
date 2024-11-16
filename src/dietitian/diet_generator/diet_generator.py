from typing import Iterable, Iterator
import random

from src.models.recipe.recipe import Recipe


class DietGenerator:
    STAGNATION_LIMIT = 1000

    def __init__(self, recipes: tuple[Recipe], kcal_goal: int, meals_number: int):
        self.recipes = recipes
        self.kcal_goal = kcal_goal
        self.meals_number = meals_number

    def generate(self, days: int = 1) -> tuple[tuple[Recipe, ...]]:
        ancestor: list[int] = self._generate_random_chromosome()
        offspring: list[int] = [genome for genome in ancestor]
        ancestor_kcal: int = sum(recipe.kcal for recipe in self.recipes)
        while True:
            self._mutate(offspring)
            # offspring_deficit = self.kcal_goal - sum(r)
            # todo: add calorie counting

    def _mutate(self, chromosome: list[int]) -> None:
        genome_idx = random.randrange(self.meals_number)
        genome_value = random.randrange(start=0, stop=len(self.recipes))
        chromosome[genome_idx] = genome_value

    def _generate_random_chromosome(self) -> list[int]:
        if len(self.recipes) < 10:
            raise ValueError("Not enough recipes. Provide at least 10 recipes.")
        return [
            random.randrange(start=0, stop=len(self.recipes))
            for _ in range(self.meals_number)
        ]

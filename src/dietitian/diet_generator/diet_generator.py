import logging
import random
import time

from src.models.recipe.recipe import Recipe


class DietGenerator:
    STAGNATION_LIMIT = 1000
    TIME_LIMIT = 10

    def __init__(self, recipes: tuple[Recipe], kcal_goal: int, meals_number: int):
        self.recipes: tuple[Recipe] = recipes
        self.kcal_goal: int = kcal_goal
        self.meals_number: int = meals_number

    def generate(self, days: int = 1) -> tuple[tuple[Recipe, ...], ...]:
        ancestor: list[int] = self._generate_random_chromosome()
        offspring: list[int] = [genome for genome in ancestor]
        ancestor_kcal_gap: int = abs(
            self.kcal_goal - sum(self.recipes[genome].kcal for genome in ancestor)
        )

        stagnation = 0
        start = time.time()
        while (stagnation < self.STAGNATION_LIMIT) and (
            time.time() - start < self.TIME_LIMIT
        ):
            self._mutate(offspring)

            offspring_kcal = sum(self.recipes[genome] for genome in offspring)
            offspring_kcal_gap = abs(self.kcal_goal - offspring_kcal)

            if offspring_kcal_gap >= ancestor_kcal_gap:
                stagnation += 1
            else:
                ancestor = offspring
                ancestor_kcal_gap = offspring_kcal_gap
                stagnation = 0

        logging.info(
            f"""
        DietGenerator report
        --------------------
        Final kcal_gap:     {ancestor_kcal_gap}
        Execution time:     {time.time() - start}
        """
        )

        return tuple([tuple([self.recipes[genome] for genome in ancestor])])

    def _mutate(self, chromosome: list[int]) -> None:
        genome_idx = random.randrange(self.meals_number)
        genome = random.randrange(start=0, stop=len(self.recipes))
        chromosome[genome_idx] = genome

    def _generate_random_chromosome(self) -> list[int]:
        if len(self.recipes) < 10:
            raise ValueError("Not enough recipes. Provide at least 10 recipes.")
        return [
            random.randrange(start=0, stop=len(self.recipes))
            for _ in range(self.meals_number)
        ]

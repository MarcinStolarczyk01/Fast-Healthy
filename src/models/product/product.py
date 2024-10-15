from dataclasses import dataclass


FAT_KCAL = 9
PROTEIN_KCAL = 4
CARBOHYDRATES_KCAL = 4


@dataclass
class Product:
    name: str
    nutrients: dict
    def __post_init__(self):
        for name in self.nutrients.keys():
            self.name = self.nutrients[name]

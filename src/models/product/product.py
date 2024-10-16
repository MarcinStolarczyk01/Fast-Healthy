from dataclasses import dataclass, field

FAT_KCAL = 9
PROTEIN_KCAL = 4
CARBOHYDRATES_KCAL = 4


@dataclass
class Product:
    name: str
    nutrients: dict = field(init=False)

    def __init__(self, name: str, nutrients: dict):
        self.name = name
        for nutrient_name, value in nutrients.items():
            setattr(self, nutrient_name, value)

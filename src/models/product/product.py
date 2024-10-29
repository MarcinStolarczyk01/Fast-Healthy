from dataclasses import dataclass

FAT_KCAL = 9
PROTEIN_KCAL = 4
CARBOHYDRATES_KCAL = 4


@dataclass
class Product:
    name: str
    nutrients: dict[str, float]

    def __post_init__(self):
        for nutrient, value in self.nutrients.items():
            setattr(self, nutrient, value)
        delattr(self, "nutrients")

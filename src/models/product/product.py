from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MacroKcalMapping:
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

    @property
    def kcal(self) -> int:

        return round(
            MacroKcalMapping.FAT_KCAL * getattr(self, "fat")
            + MacroKcalMapping.PROTEIN_KCAL * getattr(self, "protein")
            + MacroKcalMapping.CARBOHYDRATES_KCAL * getattr(self, "carbohydrates")
        )

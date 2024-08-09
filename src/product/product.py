from dataclasses import dataclass
from keywords.keywords import MacroKeywords

FAT_KCAL = 9
PROTEIN_KCAL = 4
CARBOHYDRATES_KCAL = 4


@dataclass(frozen=True)
class Product:
    fat: int
    protein: int
    carbohydrates: int

    def get_kcal(self):
        return self.fat * FAT_KCAL + self.protein * PROTEIN_KCAL + self.carbohydrates * CARBOHYDRATES_KCAL

    def get_macro(self) -> dict[str: int]:
        return {
            MacroKeywords.fat: self.fat,
            MacroKeywords.whey: self.protein,
            MacroKeywords.carbohydrates: self.carbohydrates
        }

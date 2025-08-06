from typing import List
from datetime import date
from .models import FoodEntry, NutritionSummary

# PUBLIC_INTERFACE
def calculate_nutrition_summary(entries: List[FoodEntry], for_date: date) -> NutritionSummary:
    """Calculates nutrition for a user's entries on a given date."""
    total_calories = sum(entry.calories for entry in entries if entry.date == for_date)
    total_protein = sum(entry.protein for entry in entries if entry.date == for_date)
    total_carbs = sum(entry.carbs for entry in entries if entry.date == for_date)
    total_fat = sum(entry.fat for entry in entries if entry.date == for_date)
    return NutritionSummary(
        date=for_date,
        total_calories=total_calories,
        total_protein=total_protein,
        total_carbs=total_carbs,
        total_fat=total_fat
    )

# PUBLIC_INTERFACE
def calculate_nutrition_history(entries: List[FoodEntry]) -> List[NutritionSummary]:
    """Aggregates entries by date for a historical chart."""
    by_date = {}
    for entry in entries:
        d = entry.date
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(entry)

    summaries = []
    for single_date, entries_on_date in sorted(by_date.items()):
        summaries.append(calculate_nutrition_summary(entries_on_date, single_date))
    return summaries

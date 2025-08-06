from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from .models import FoodEntry, FoodEntryCreate, FoodEntryUpdate

# In-memory food storage. Key: user_email, Value: List[FoodEntry]
_food_db = {}
_entry_id_counter = {"id": 1}

def _next_entry_id():
    eid = _entry_id_counter["id"]
    _entry_id_counter["id"] += 1
    return eid

# PUBLIC_INTERFACE
def list_food_entries(user_email: str, for_date: Optional[date] = None) -> List[FoodEntry]:
    """List food entries for a user optionally filtered by date."""
    user_entries = _food_db.get(user_email, [])
    if for_date:
        return [entry for entry in user_entries if entry.date == for_date]
    return user_entries

# PUBLIC_INTERFACE
def get_food_entry(user_email: str, entry_id: int) -> FoodEntry:
    """Retrieve a food entry by ID for the user."""
    for entry in _food_db.get(user_email, []):
        if entry.id == entry_id:
            return entry
    raise HTTPException(status_code=404, detail="Food entry not found")

# PUBLIC_INTERFACE
def create_food_entry(user_email: str, entry: FoodEntryCreate) -> FoodEntry:
    """Create a new food entry for a user."""
    eid = _next_entry_id()
    food = FoodEntry(id=eid, **entry.model_dump())
    if user_email not in _food_db:
        _food_db[user_email] = []
    _food_db[user_email].append(food)
    return food

# PUBLIC_INTERFACE
def update_food_entry(user_email: str, entry_id: int, entry: FoodEntryUpdate) -> FoodEntry:
    """Update an existing food entry."""
    entries = _food_db.get(user_email, [])
    for idx, existing in enumerate(entries):
        if existing.id == entry_id:
            updated_data = existing.model_dump()
            update_dict = entry.model_dump(exclude_unset=True)
            updated_data.update(update_dict)
            updated_food = FoodEntry(**updated_data)
            entries[idx] = updated_food
            return updated_food
    raise HTTPException(status_code=404, detail="Food entry not found")

# PUBLIC_INTERFACE
def delete_food_entry(user_email: str, entry_id: int):
    """Delete a food entry."""
    entries = _food_db.get(user_email, [])
    for idx, entry in enumerate(entries):
        if entry.id == entry_id:
            del entries[idx]
            return
    raise HTTPException(status_code=404, detail="Food entry not found")

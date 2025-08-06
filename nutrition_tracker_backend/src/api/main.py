from fastapi import FastAPI, Depends, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from datetime import date

from .models import (
    UserRegister,
    Token,
    FoodEntry,
    FoodEntryCreate,
    FoodEntryUpdate,
    NutritionSummary,
    NutritionHistory,
    Message,
)
from .auth import (
    login,
    register,
    get_current_user,
)
from .food import (
    list_food_entries,
    get_food_entry,
    create_food_entry,
    update_food_entry,
    delete_food_entry,
)
from .nutrition import (
    calculate_nutrition_summary,
    calculate_nutrition_history,
)

app = FastAPI(
    title="Nutrition Tracker API",
    description="Backend for food logging/nutrition tracking with JWT authentication",
    version="0.1.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication and user management"},
        {"name": "food", "description": "Food entry CRUD operations"},
        {"name": "dashboard", "description": "Nutrition dashboard and summary"},
        {"name": "analytics", "description": "Nutrition analytics endpoints"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}

# === AUTH ENDPOINTS ===

@app.post("/auth/register", response_model=Message, tags=["auth"], summary="Register User", description="Register a new user account.")
async def register_user(data: UserRegister):
    await register(data)
    return Message(detail="Registration successful")

@app.post("/auth/token", response_model=Token, tags=["auth"], summary="Login User", description="Obtain JWT access token via login credentials.")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await login(form_data)
    return Token(**result)

# === FOOD ENDPOINTS ===
@app.post("/food", response_model=FoodEntry, tags=["food"], summary="Add Food Entry", description="Create a new food log entry for the current user.")
def add_food_entry(
    entry: FoodEntryCreate,
    user: dict = Depends(get_current_user)
):
    return create_food_entry(user_email=user["email"], entry=entry)

@app.get("/food", response_model=List[FoodEntry], tags=["food"], summary="List Food Entries", description="List food entries for the current user, optionally filtered by date.")
def list_food(
    date_filter: Optional[date] = Query(None, description="(Optional) Date to filter entries"),
    user: dict = Depends(get_current_user)
):
    return list_food_entries(user_email=user["email"], for_date=date_filter)

@app.get("/food/{entry_id}", response_model=FoodEntry, tags=["food"], summary="Get Food Entry", description="Get a specific food entry by ID.")
def get_food(
    entry_id: int = Path(..., ge=1),
    user: dict = Depends(get_current_user)
):
    return get_food_entry(user_email=user["email"], entry_id=entry_id)

@app.put("/food/{entry_id}", response_model=FoodEntry, tags=["food"], summary="Edit Food Entry", description="Edit an existing food entry by ID.")
def update_food(
    entry_id: int = Path(..., ge=1),
    entry: FoodEntryUpdate = ...,
    user: dict = Depends(get_current_user)
):
    return update_food_entry(user_email=user["email"], entry_id=entry_id, entry=entry)

@app.delete("/food/{entry_id}", response_model=Message, tags=["food"], summary="Delete Food Entry", description="Delete a food entry by ID.")
def delete_food(
    entry_id: int = Path(..., ge=1),
    user: dict = Depends(get_current_user)
):
    delete_food_entry(user_email=user["email"], entry_id=entry_id)
    return Message(detail="Food entry deleted")

# === DASHBOARD/ANALYTICS ENDPOINTS ===

@app.get("/dashboard", response_model=NutritionSummary, tags=["dashboard"], summary="Daily Nutrition Dashboard", description="Returns nutritional summary for the user for given day (defaults to today).")
def dashboard(
    for_date: Optional[date] = Query(None, description="Date for the dashboard (defaults to today)"),
    user: dict = Depends(get_current_user)
):
    if for_date is None:
        for_date = date.today()
    entries = list_food_entries(user_email=user["email"], for_date=for_date)
    return calculate_nutrition_summary(entries, for_date)

@app.get("/analytics/history", response_model=NutritionHistory, tags=["analytics"], summary="Nutrition History", description="Returns user's nutrition stats/history for visual analytics.")
def nutrition_history(
    user: dict = Depends(get_current_user)
):
    entries = list_food_entries(user_email=user["email"])
    summaries = calculate_nutrition_history(entries)
    return NutritionHistory(summaries=summaries)

# === SIMPLE CALORIE/MACRO API ===

@app.get("/tracking/macros", tags=["dashboard"], summary="Get Current Macros", description="Fetch and calculate total calories/macros for a given day.", response_model=NutritionSummary)
def fetch_macros(
    for_date: Optional[date] = Query(None, description="Date to fetch calories/macros for (defaults to today)"),
    user: dict = Depends(get_current_user)
):
    if for_date is None:
        for_date = date.today()
    entries = list_food_entries(user_email=user["email"], for_date=for_date)
    return calculate_nutrition_summary(entries, for_date)

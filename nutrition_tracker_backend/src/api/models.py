# PUBLIC_INTERFACE
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date

# PUBLIC_INTERFACE
class UserRegister(BaseModel):
    """Schema for registering a new user."""
    email: EmailStr = Field(..., description="User email for registration")
    password: str = Field(..., min_length=6, description="Password for the user")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email for login")
    password: str = Field(..., description="Password for the user")

# PUBLIC_INTERFACE
class Token(BaseModel):
    """JWT response token model."""
    access_token: str
    token_type: str

# PUBLIC_INTERFACE
class TokenData(BaseModel):
    """Payload for user in JWT."""
    email: Optional[EmailStr] = None

# PUBLIC_INTERFACE
class FoodEntryBase(BaseModel):
    """Base fields for food entry."""
    name: str = Field(..., description="Name of the food consumed")
    quantity: float = Field(..., gt=0, description="Serving quantity (e.g., grams)")
    calories: float = Field(..., ge=0, description="Calories for the portion entered")
    protein: float = Field(..., ge=0, description="Protein (g)")
    carbs: float = Field(..., ge=0, description="Carbohydrates (g)")
    fat: float = Field(..., ge=0, description="Fat (g)")
    date: date = Field(..., description="Date of consumption")

# PUBLIC_INTERFACE
class FoodEntryCreate(FoodEntryBase):
    """Input schema for creating a food entry."""
    pass

# PUBLIC_INTERFACE
class FoodEntryUpdate(BaseModel):
    """Editable fields for updating a food entry."""
    name: Optional[str]
    quantity: Optional[float]
    calories: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fat: Optional[float]

# PUBLIC_INTERFACE
class FoodEntry(FoodEntryBase):
    """Output schema for food entry."""
    id: int

# PUBLIC_INTERFACE
class NutritionSummary(BaseModel):
    """Aggregate summary for a day or a period."""
    date: date
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float

# PUBLIC_INTERFACE
class NutritionHistory(BaseModel):
    """Nutrition history/analytics model."""
    summaries: List[NutritionSummary]

# PUBLIC_INTERFACE
class Message(BaseModel):
    """Simple message for status responses."""
    detail: str

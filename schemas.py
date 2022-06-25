from pydantic import BaseModel, HttpUrl
from typing import Sequence
    
class MealType(BaseModel):
    id: int
    label: str

class Meal(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl

class MealSearchResults(BaseModel):
    results: Sequence[Meal]

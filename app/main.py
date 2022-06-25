from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates
from typing import Optional, Any
from pathlib import Path
from schemas import MealSearchResults, Meal#, MealCreate
from meal_data import MEALS

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Meal Planning API", openapi_url="/openapi.json")

api_router = APIRouter()

@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root Get
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "meals": MEALS},
    )

@api_router.get("/meal/{meal_id}", status_code=200, response_model=Meal)
def fetch_recipe(*, meal_id: int) -> dict:
    """
    Fetch a single meal by ID
    """

    result = [meal for meal in MEALS if meal["id"] == meal_id]
    if result:
        raise HTTPException(
                status_code=404, detail=f"Recipe with ID {meal_id} not found"
            )
    return result[0]

@api_router.get("/search/", status_code=200, response_model=MealSearchResults)
def search_meals(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),  # 2
    max_results: Optional[int] = 10
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": MEALS[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), MEALS)
    return {"results": list(results)[:max_results]}


app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    print("Debugger starting, access @ http://127.0.0.1:8001/docs")
    import uvicorn
    print("Press Control-C to exit", end="...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
    print("application ended.")
    
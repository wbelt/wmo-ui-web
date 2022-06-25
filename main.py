import os
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates
from typing import Optional, Any
from pathlib import Path
from schemas import MealSearchResults, Meal#, MealCreate
from meal_data import MEALS
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

TEMPLATES = Jinja2Templates(directory=str("templates"))

app = FastAPI(title="Meal Planning API", openapi_url="/openapi.json")
FastAPIInstrumentor().instrument_app(app)

@app.get("/", status_code=200)
async def dashboard_page(request: Request) -> dict:
    """
    The primary dashboard to view meals and access plans.
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "meals": MEALS}
    )

@app.get("/status", status_code=200)
async def static_status_page(request: Request) -> dict:
    """
    A simple static status page that can be used by helth checks or other monitors to verify uptime.
    """
    return TEMPLATES.TemplateResponse(
        "status.html",
        {"request": request}
    )

@app.get("/meal/{meal_id}", status_code=200, response_model=Meal)
async def fetch_recipe(*, meal_id: int) -> dict:
    """
    Fetch a single meal by ID
    """

    result = [meal for meal in MEALS if meal["id"] == meal_id]
    if not result:
        raise HTTPException(
                status_code=404, detail=f"Meal with ID {meal_id} not found"
            )
    return result[0]

@app.get("/search/", status_code=200, response_model=MealSearchResults)
async def search_meals(*,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10) -> dict:
    """
    Search for meals by label keyword
    """
    if not keyword:
        return {"results": MEALS[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), MEALS)
    return {"results": list(results)[:max_results]}

if __name__ == "__main__":
    # Use this for debugging purposes only
    print("Debugger starting, access @ http://127.0.0.1:8001/docs")
    import uvicorn
    print("Press Control-C to exit", end="...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
    print("application ended.")

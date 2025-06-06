# artisan_ai_backend/app/main.py
from fastapi import FastAPI

from . import models
from .database import engine 
# Import your routers
from .routers import configurations, auth, llm_suggestions # <--- ADD llm_suggestions

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ArtisanAI Backend",
    description="API for ArtisanAI to manage prompt configurations, users, LLM suggestions, and advanced prompt crafting.",
    version="0.4.0", # Version bump for new feature
)

# Include your API routers
app.include_router(auth.router) 
app.include_router(configurations.router)
app.include_router(llm_suggestions.router) # <--- ADD THIS NEW ROUTER
# We will add prompt_crafter_router here in the next phase

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for the ArtisanAI Backend.
    Provides a welcome message.
    """
    return {"message": "Welcome to the ArtisanAI Backend! Navigate to /docs for API documentation."}

@app.get("/hello/{name}", tags=["General Testing"])
async def say_hello(name: str):
    """
    A simple endpoint to test if the server is responding.
    """
    return {"message": f"Hello, {name} from ArtisanAI Backend!"}
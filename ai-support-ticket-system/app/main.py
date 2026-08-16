from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tickets import router as tickets_router


app = FastAPI(title="AI Support Ticket System", version="0.2.0")
app.include_router(auth_router)
app.include_router(tickets_router)


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"message": "AI Support Ticket System is running"}

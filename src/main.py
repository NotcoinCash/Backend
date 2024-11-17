from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from src.admin.admin import init_admin
from src.database import async_session_factory
from src.models import Token
from src.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
init_admin(app)

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/token")
async def get_token_info():
    async with async_session_factory() as session:
        result = await session.execute(select(Token).limit(1))
        token = result.scalars().first()
        if token is None:
            return {"status": "error", "message": "Token info is not set"}

    return {
        "status": "success",
        "message": "Token info is fetched successfully",
        "data": {
            "total_supply": token.total_supply,
            "total_supply_percent": 100,
            "developers": token.developers,
            "developers_percent": (token.developers / token.total_supply) * 100,
            "community": token.community,
            "community_percent": (token.community / token.total_supply) * 100,
            "mined": token.mined,
            "mined_percent": (token.mined / token.total_supply) * 100,
        }
    }

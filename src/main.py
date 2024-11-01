from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin.admin import init_admin
from src.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
init_admin(app)

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def index():
    return {"Hello": "World"}
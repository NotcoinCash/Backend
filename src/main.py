from fastapi import FastAPI

from src.admin import init_admin

app = FastAPI()
init_admin(app)


@app.get("/")
def index():
    return {"Hello": "World"}

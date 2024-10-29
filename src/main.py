from fastapi import FastAPI

from src.admin.admin import init_admin

app = FastAPI()
init_admin(app)


@app.get("/")
def index():
    return {"Hello": "World"}

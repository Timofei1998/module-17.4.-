from fastapi import FastAPI
from backend.user import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
@app.get("/")
def read_root():
    return {"message": "Welcome to the User API!"}

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.router import book, user


app = FastAPI()

app.include_router(book.router, prefix="/books")
app.include_router(user.router, prefix="/users")


@app.get("/")
def read_root():
    return RedirectResponse("/docs")

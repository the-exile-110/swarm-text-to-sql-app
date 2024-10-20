from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager
from database import Database
from agents import process_query

app = FastAPI()

templates = Jinja2Templates(directory="templates")

db = Database()

def get_db():
    with db.get_cursor() as cursor:
        yield cursor

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query(user_input: str = Form(...), cursor = Depends(get_db)):
    result = process_query(user_input, cursor)
    return JSONResponse(content=result)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await shutdown_event()
    yield

async def shutdown_event():
    if db.conn:
        db.conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

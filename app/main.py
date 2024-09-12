from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints
from app.db.database import engine, Base
from pathlib import Path
# all sorts of project starting stuff

app = FastAPI()

# create table
Base.metadata.create_all(bind=engine)

# add static
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# add API routes
app.include_router(endpoints.router)

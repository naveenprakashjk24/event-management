
import os
import sys

# Add the parent directory of blog to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import models
from database import engine
from fastapi import FastAPI
from routers import authentication, events, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(events.router)
app.include_router(users.router)

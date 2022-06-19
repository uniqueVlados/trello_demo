from fastapi import FastAPI

from website import models
from website.database import engine
from website.routers import views

app = FastAPI()


models.Base.metadata.create_all(engine)
app.include_router(views.router)
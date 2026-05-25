from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from src.controllers.contact_controller import contact_router

load_dotenv()

app_env = os.getenv('APP_ENV')
is_local = (app_env == 'local')

app = FastAPI(
    title='Contact Book API',
    version='1.0.0',
    description='All API endpoints for Contact Book',
    docs_url="/docs",  # បើកជានិច្ច
    redoc_url="/redoc" # បើកជានិច្ច
)
app.mount('/upload', StaticFiles(directory='upload'), name='upload')


app.include_router(contact_router)
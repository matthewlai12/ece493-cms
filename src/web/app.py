from fastapi import FastAPI

from src.web.routes import router as web_router

app = FastAPI(title="CMS Web")
app.include_router(web_router)

from fastapi import FastAPI

from src.api.middleware.rbac import require_role
from src.api.routes import router as api_router

app = FastAPI(title="CMS API")
app.middleware("http")(require_role)
app.include_router(api_router)

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import system
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.events import router as events_router
from app.routers.twins import router as twins_router
from app.routers.dashboard import router as dashboard_router
from app.routers.admin import router as admin_router
from app.routers.insights import router as insights_router
from app.routers.alerts import router as alerts_router
from app.routers.linked_accounts import router as linked_accounts_router
from app.routers.sessions import router as session_router
from app.core.error_handler import register_error_handlers
from fastapi.responses import JSONResponse
from fastapi import Request
from app.db.init_db import init_db


load_dotenv()

app = FastAPI(
    title="Digital Class Twin Backend",
    swagger_ui_parameters={"persistAuthorization": True}
)
init_db()

register_error_handlers(app)

app.security = [HTTPBearer()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(events_router)
app.include_router(twins_router)
app.include_router(dashboard_router)
app.include_router(admin_router)
app.include_router(insights_router)
app.include_router(alerts_router)
app.include_router(linked_accounts_router)
app.include_router(session_router)
app.include_router(system.router)

@app.get("/")
def health():
    return {"status": "backend running"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )

from fastapi import FastAPI
from src.tasks.router import task_routes
from src.user.router import user_routes
from src.utils.exceptions import AppException, app_exception_handler, generic_exception_handler
from src.utils.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

# Setup logging
setup_logging()

app = FastAPI(
    title="Task Management API",
    description="A production-ready task management API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(task_routes, tags=["Tasks"])
app.include_router(user_routes, tags=["Users"])

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
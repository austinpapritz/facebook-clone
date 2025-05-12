from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.init_db import init_db
from app.api.v1.routes import user, post, comment

app = FastAPI(title="Facebook Clone API", version="1.0.0")

# Erase init_db() once real user data is used
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Shutdown: Could add cleanup code here

app = FastAPI(
    title="Facebook Clone API", 
    version="1.0.0",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(post.router, prefix="/api/v1", tags=["posts"])
app.include_router(comment.router, prefix="/api/v1", tags=["comments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Facebook Clone API"}


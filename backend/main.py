from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import lease, violations, letters

app = FastAPI(
    title="RentGhost",
    description="AI agent that reads your lease, finds landlord violations, and drafts legal letters.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lease.router, prefix="/api/lease", tags=["Lease"])
app.include_router(violations.router, prefix="/api/violations", tags=["Violations"])
app.include_router(letters.router, prefix="/api/letters", tags=["Letters"])


@app.get("/")
async def root():
    return {"app": "RentGhost", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}

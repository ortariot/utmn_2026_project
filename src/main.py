import uvicorn
from fastapi import FastAPI

from api.v1.misk import router as misk_router
from api.v1.charendpoints import router as char_router

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)


app.include_router(misk_router, prefix="/api/v1/misk", tags=["misk"])
app.include_router(char_router, prefix="/api/v1/char", tags=["char"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
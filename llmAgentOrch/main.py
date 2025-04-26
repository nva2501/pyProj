from fastapi import FastAPI
from app.api import router
from app.metrics.prometheus_instrumentation import instrumentator

app = FastAPI()

app.include_router(router.router)

@app.on_event("startup")
async def startup():
    instrumentator.instrument(app).expose(app)

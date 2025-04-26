from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from app.models.request_model import RequestInput
from app.services.classifier_service import ClassifierService
from app.services.agent_router_service import AgentRouterService
from app.services.auth_service import AuthService
from app.services.rate_limiter_service import RateLimiterService
from app.utils.context_manager import disconnect_checker
from app.models.retrain_model import RetrainInput
import asyncio

router = APIRouter()
classifier = ClassifierService()
router_service = AgentRouterService()
rate_limiter = RateLimiterService()

@router.post("/route")
async def route_request(
    request: Request,
    data: RequestInput,
    x_api_key: str = Header(...)
):
    # Authentication
    if not AuthService.validate(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Rate Limiting
    if not rate_limiter.is_allowed(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Disconnection Handler
    task = asyncio.create_task(disconnect_checker(request))

    async def stream_response():
        try:
            request_type = classifier.predict(data.text)
            yield f"Identified Type: {request_type}\n"
            response = await router_service.route(request_type, data.text)
            yield f"Response: {response}\n"
        except asyncio.CancelledError:
            yield "Request was cancelled by client.\n"
        finally:
            task.cancel()

    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/retrain")
async def retrain_model(data: RetrainInput, x_api_key: str = Header(...)):
    # Authentication
    if not AuthService.validate(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Rate Limiting
    if not rate_limiter.is_allowed(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    classifier.add_training_example(data.text, data.label)
    return {"message": "New example added and classifier updated."}
from connector.helpers import collect_methods
from connector.integration import Integration


def collect_routes(obj: object):
    """
    Collect all methods from an object and create a route for each.
    """
    from fastapi import APIRouter

    router = APIRouter()
    commands = collect_methods(obj)
    for method in commands:
        router.add_api_route(f"/{method.__name__.replace('_', '-')}", method, methods=["POST"])
    return router


def collect_integration_routes(integration: Integration):
    """Create API endpoint for each method in integration."""
    from fastapi import APIRouter

    router = APIRouter()
    for capability_name, capability in integration.capabilities.items():
        router.add_api_route(f"/{capability_name}", capability, methods=["POST"])

    return router


def runserver(router, port: int):
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, port=port)

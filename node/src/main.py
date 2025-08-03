from fastapi import FastAPI
from fastapi.routing import APIRoute

from .wireguard.router import router as wireguard_router
from .wstunnel.router import router as wstunnel_router

app = FastAPI()
app.include_router(wireguard_router)
app.include_router(wstunnel_router)

# Modify for autogenerator
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name

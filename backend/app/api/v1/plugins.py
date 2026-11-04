from fastapi import APIRouter
from app.services.plugin_catalog import get_plugins
from app.models.plugin import PluginListResponse

router = APIRouter()


@router.get("/plugins", response_model=PluginListResponse)
async def list_plugins() -> PluginListResponse:
    return get_plugins()

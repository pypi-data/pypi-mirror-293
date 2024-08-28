from fastapi import APIRouter, Request

from promptadmin.sync.collector import collect
from promptadmin.types import ProjectPromptInfo
from settings import SETTINGS

router = APIRouter()


@router.get('/prompt-admin/collect', response_model=ProjectPromptInfo)
async def get_collect(request: Request):
    if request.headers.get('Prompt-Admin-Secret', None) != SETTINGS.prompt_admin_settings.router_secret:
        raise ValueError()
    return collect()

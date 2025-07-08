from typing import List

from fastapi import APIRouter

from fp_admin.admin.apps import AppInfo, apps_info

apps_api = APIRouter()


@apps_api.get("/")
def list_apps() -> List[AppInfo]:
    return apps_info()

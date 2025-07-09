from typing import Any, List

from fp_admin.admin.models import model_registry
from fp_admin.settings_loader import settings

from .app_config import apps_registry
from .schema import AppInfo, ModelInfo


def apps_info() -> List[AppInfo]:
    apps = []

    models = model_registry.all() or []
    for app, config in apps_registry.all().items():
        apps.append(app_info(app, config.verbose_name, models))
    return apps


def app_info(app: str, appl_label: str, models: List[dict[str, Any]]) -> AppInfo:
    api_router_prefix = f"{settings.ADMIN_PATH}/{settings.API_VERSION}"
    models = [model for model in models if app == model.get("app")]
    app_models = []
    for model in models:
        model_name = model.get("model_name", "")
        app_models.append(
            ModelInfo(
                name=model_name,
                label=model.get("model_label", ""),
                url=f"{api_router_prefix}/models/{model_name}",
            )
        )
    return AppInfo(name=app, label=appl_label, models=app_models)

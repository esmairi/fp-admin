from typing import TYPE_CHECKING, Dict, List

from fp_admin.registry import apps_registry
from fp_admin.settings_loader import settings

from .schema import AppInfo, ModelInfo

if TYPE_CHECKING:
    from fp_admin.registry.admin_model_config import AdminModelConfig


def apps_info() -> List[AppInfo]:
    apps = []
    from fp_admin.registry import model_registry

    models: Dict[str, "AdminModelConfig"] = model_registry.list() or {}
    for app, config in apps_registry.list().items():
        apps.append(app_info(app, config.verbose_name, models))
    return apps


def app_info(
    app: str, app_label: str, models_info: Dict[str, "AdminModelConfig"]
) -> AppInfo:
    api_router_prefix = f"{settings.ADMIN_PATH}/{settings.API_VERSION}"
    models: List["AdminModelConfig"] = [
        model for model in models_info.values() if app == model.app
    ]
    app_models = []
    for model in models:
        model_name = model.name
        app_models.append(
            ModelInfo(
                name=model_name,
                label=model.label,
                url=f"{api_router_prefix}/models/{model_name}",
            )
        )
    return AppInfo(name=app, label=app_label, models=app_models)

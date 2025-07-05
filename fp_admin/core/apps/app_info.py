from typing import List

from fp_admin.apps.auth.models import App, BasicModel
from fp_admin.core.apps.app_config import apps_registry
from fp_admin.core.models.base import admin_model_registry


def app_info() -> List[App]:
    apps = []
    models = admin_model_registry.all() or []
    for app, config in apps_registry.all().items():
        app_models = [
            BasicModel(name=model.model_name, label=model.model_label)
            for model in models
            if app == model.apps
        ]
        apps.append(
            App(
                model_name=app,
                model_label=config.verbose_name,
                model=app_models,
                apps="",
            )
            # {"name": app, "label": config.verbose_name, "models": app_models}
        )
    return apps

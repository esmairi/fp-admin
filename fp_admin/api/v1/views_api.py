from typing import Dict, List, cast

from fastapi import APIRouter

from fp_admin.admin.views import view_registry
from fp_admin.api.v1.schemas.views import (
    BaseViewInstanceSchema,
    BaseViewSchema,
    ModelViewsResponseSchema,
    ViewsResponseSchema,
)

views_api = APIRouter()


@views_api.get(
    "/",
    response_model=ViewsResponseSchema,
    response_model_exclude_none=True,
    summary="Get all views",
    description="Retrieve all registered views organized by model name",
)
def get_views() -> ViewsResponseSchema:
    """Get all registered views."""
    views_data = view_registry.all()
    # Convert BaseView objects to appropriate schema for proper serialization
    serialized_views: Dict[str, List[BaseViewInstanceSchema]] = {}
    for model_name, views in views_data.items():
        serialized_views[model_name] = [
            BaseViewSchema.serialize_view(cast(BaseViewSchema, view)) for view in views
        ]
    return ViewsResponseSchema(data=serialized_views)


@views_api.get(
    "/{model_name}",
    response_model=ModelViewsResponseSchema,
    response_model_exclude_none=True,
    summary="Get model views",
    description="Retrieve all views for a specific model",
)
async def get_model_views(model_name: str) -> ModelViewsResponseSchema:
    """Get views for a specific model."""
    views = [
        BaseViewSchema.serialize_view(cast(BaseViewSchema, view))
        for view in view_registry.get(model_name)
    ]
    return ModelViewsResponseSchema(data=views)

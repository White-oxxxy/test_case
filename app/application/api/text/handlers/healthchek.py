from fastapi import status

from .common import router
from application.api.text.schemas import HealthCheckOutSchema


@router.get(
    path="/health",
    status_code=status.HTTP_200_OK,
    description="Проверка работоспособности апи",
    include_in_schema=False,
)
async def health() -> HealthCheckOutSchema:
    schema = HealthCheckOutSchema(status="ok")

    return schema
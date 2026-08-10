from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_category_service
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[Category])
def get_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[Category]:
    return service.list_categories()


@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
) -> Category:
    return service.create_category(payload)


@router.patch("/{category_id}", response_model=Category)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
) -> Category:
    return service.update_category(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service),
) -> None:
    service.delete_category(category_id)

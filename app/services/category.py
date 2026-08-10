from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import Category, CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repo = CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        categories = self.category_repo.get_all()
        return [Category.model_validate(category) for category in categories]

    def create_category(self, category_create: CategoryCreate) -> Category:
        category = self.category_repo.create(name=category_create.name)
        self.db.commit()
        return Category.model_validate(category)

    def update_category(
        self, category_id: str, category_update: CategoryUpdate
    ) -> Category:
        category_for_update = self.category_repo.get_by_id(category_id=category_id)
        if category_for_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        category_for_update.name = (
            category_update.name
            if category_update.name is not None
            else category_for_update.name
        )
        self.db.commit()
        return Category.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repo.get_by_id(category_id=category_id)
        if category_for_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        self.category_repo.delete(category_for_delete)
        self.db.commit()

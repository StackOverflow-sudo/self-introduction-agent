from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def list(self) -> list[Project]:
        return (
            self.db.query(Project)
            .order_by(Project.sort_order.asc(), Project.id.asc())
            .all()
        )

    def create(self, data: ProjectCreate) -> Project:
        obj = Project(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, project_id: int, data: ProjectUpdate) -> Project | None:
        obj = self.get(project_id)
        if obj is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, project_id: int) -> bool:
        obj = self.get(project_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

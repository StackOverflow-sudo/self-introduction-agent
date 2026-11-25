from sqlalchemy.orm import Session

from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def get(self, project_id: int):
        return self.repo.get(project_id)

    def list(self):
        return self.repo.list()

    def create(self, data: ProjectCreate):
        return self.repo.create(data)

    def update(self, project_id: int, data: ProjectUpdate):
        return self.repo.update(project_id, data)

    def delete(self, project_id: int):
        return self.repo.delete(project_id)

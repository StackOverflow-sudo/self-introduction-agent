from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.services.project import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])


def get_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.get("", response_model=list[ProjectOut])
def list_projects(svc: ProjectService = Depends(get_service)):
    return svc.list()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, svc: ProjectService = Depends(get_service)):
    obj = svc.get(project_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="project not found")
    return obj


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, svc: ProjectService = Depends(get_service)):
    return svc.create(data)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, svc: ProjectService = Depends(get_service)):
    obj = svc.update(project_id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="project not found")
    return obj


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, svc: ProjectService = Depends(get_service)):
    if not svc.delete(project_id):
        raise HTTPException(status_code=404, detail="project not found")

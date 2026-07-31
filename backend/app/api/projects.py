import asyncio, json
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, selectinload
from app.api.deps import get_current_user
from app.db.session import SessionLocal, get_db
from app.models import Project
from app.schemas.schemas import ProjectCreate, ProjectRead
from app.services.agent_runner import seed_agents, run_project, zip_project
router = APIRouter(prefix="/projects", tags=["projects"])
def owned(db, project_id, user_id):
    project = db.query(Project).options(selectinload(Project.agents), selectinload(Project.logs)).filter(Project.id==project_id, Project.owner_id==user_id).first()
    if not project: raise HTTPException(404, "Project not found")
    return project
@router.get("", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Project).options(selectinload(Project.agents), selectinload(Project.logs)).filter(Project.owner_id==user.id).order_by(Project.created_at.desc()).all()
@router.post("", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = Project(name=payload.name, idea=payload.idea, owner_id=user.id); db.add(project); db.commit(); db.refresh(project); seed_agents(db, project); return owned(db, project.id, user.id)
@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)): return owned(db, project_id, user.id)
@router.post("/{project_id}/execute", response_model=ProjectRead)
def execute(project_id: int, background: BackgroundTasks, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = owned(db, project_id, user.id)
    if project.status == "running": return project
    background.add_task(run_project, SessionLocal, project_id)
    project.status = "queued"; db.commit(); return owned(db, project_id, user.id)
@router.get("/{project_id}/stream")
async def stream(project_id: int, token: str, db: Session = Depends(get_db)):
    from app.api.deps import get_current_user
    user = get_current_user(token, db); owned(db, project_id, user.id)
    async def events():
        last = ""
        while True:
            fresh = owned(db, project_id, user.id)
            payload = ProjectRead.model_validate(fresh).model_dump(mode="json")
            data = json.dumps(payload)
            if data != last:
                yield f"data: {data}\n\n"; last = data
            if fresh.status in {"completed", "failed"}: break
            await asyncio.sleep(0.8); db.expire_all()
    return StreamingResponse(events(), media_type="text/event-stream")
@router.get("/{project_id}/download")
def download(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = owned(db, project_id, user.id); buf = zip_project(project)
    return StreamingResponse(buf, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={project.name.replace(' ', '-')}.zip"})

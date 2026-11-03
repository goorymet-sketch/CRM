from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Reach CRM", version="0.1.0",
              description="CRM for managing companies, leads, and sales follow-ups.")

@app.get("/health")
def health():
    return {"status": "ok", "service": "digital-reach-crm"}

@app.get("/")
def root():
    return {"name": "Digital Reach CRM", "docs": "/docs", "health": "/health"}

@app.post("/companies", response_model=schemas.CompanyRead, status_code=201)
def create_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db)):
    company = models.Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@app.get("/companies", response_model=list[schemas.CompanyRead])
def list_companies(q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(models.Company).order_by(models.Company.name)
    if q:
        stmt = stmt.where(models.Company.name.ilike(f"%{q}%"))
    return db.scalars(stmt).all()

@app.post("/leads", response_model=schemas.LeadRead, status_code=201)
def create_lead(payload: schemas.LeadCreate, db: Session = Depends(get_db)):
    if db.get(models.Company, payload.company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    lead = models.Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@app.get("/leads", response_model=list[schemas.LeadRead])
def list_leads(status: str | None = None, db: Session = Depends(get_db)):
    stmt = select(models.Lead).order_by(models.Lead.created_at.desc())
    if status:
        stmt = stmt.where(models.Lead.status == status)
    return db.scalars(stmt).all()

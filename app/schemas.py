from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    website: str | None = None
    industry: str | None = None
    country: str | None = None
    notes: str | None = None

class CompanyRead(CompanyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class LeadCreate(BaseModel):
    company_id: int
    title: str = Field(min_length=1, max_length=180)
    status: str = "new"
    source: str | None = None
    expected_value: str | None = None
    next_follow_up: datetime | None = None
    notes: str | None = None

class LeadRead(LeadCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

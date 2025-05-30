from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any

class ResumeCreateSchema(BaseModel):
    name: str
    gender: str
    age: int
    degree: str
    skills: Optional[str]
    job_target: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    file_path: Optional[str]
    parse_json: Optional[Any]

class ResumeUpdateSchema(ResumeCreateSchema):
    status: Optional[str]

class ResumeResponseSchema(ResumeCreateSchema):
    resume_id: int
    status: str

    class Config:
        orm_mode = True

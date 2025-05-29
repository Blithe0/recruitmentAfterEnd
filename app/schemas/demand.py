# schemas/demand.py
from pydantic import BaseModel

class DemandCreateSchema(BaseModel):
    job_name: str
    job_type: str
    job_place: str
    demand_number: int
    job_description: str
    job_requirement: str
    reason: str

class DemandUpdateSchema(DemandCreateSchema):
    pass

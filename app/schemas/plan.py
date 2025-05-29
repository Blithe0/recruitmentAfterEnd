# schemas/plan.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# 创建招聘计划时使用
class PlanCreateSchema(BaseModel):
    demand_id: int = Field(..., description="关联的招聘需求ID")
    user_id: int = Field(..., description="创建人用户ID")
    recruit_number: int = Field(..., gt=0, description="招聘人数")
    release_time: date = Field(..., description="发布时间")
    use_time: date = Field(..., description="拟用人时间")
    salary: str = Field(..., description="薪资范围")
    job_name: str = Field(..., description="岗位名称")

# 用于返回计划信息
class PlanResponseSchema(PlanCreateSchema):
    plan_id: int = Field(..., description="计划ID")
    plan_status: str = Field(..., description="计划状态")


# app/schemas/selection.py
from marshmallow import Schema, fields, post_dump
from app.models.selection import Selection

class SelectionSchema(Schema):
    # id = fields.Int(attribute='selection_id')
    selection_id = fields.Int()
    plan_id = fields.Int()
    steps = fields.Method("get_steps", deserialize="load_steps")
    job_name = fields.Method("get_job_name")

    def get_steps(self, obj):
        return obj.steps_json

    def load_steps(self, value):
        return value

    def get_job_name(self, obj):
        return obj.plan.job_name if obj.plan else None

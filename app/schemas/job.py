from marshmallow import Schema, fields

class JobSchema(Schema):
    job_id = fields.Int(dump_only=True)
    plan_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    pass_number = fields.Int()
    job_status = fields.Str()

    # 附带计划详情（岗位名等）
    job_name = fields.Str(dump_only=True)
    recruit_number = fields.Int(dump_only=True)
    job_place = fields.Str(dump_only=True)
    job_description = fields.Str(dump_only=True)
    job_requirement = fields.Str(dump_only=True)
    salary = fields.Str(dump_only=True)

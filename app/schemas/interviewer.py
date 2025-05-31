from marshmallow import Schema, fields

class InterviewerSchema(Schema):
    interviewer_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    department_id = fields.Str(required=True)
    contact = fields.Str()

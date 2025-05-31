from marshmallow import Schema, fields

class InterviewSchema(Schema):
    interview_id = fields.Int(dump_only=True)
    candidate_id = fields.Int(required=True)
    interviewer_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    job_id = fields.Int(required=True)
    interviewer_time = fields.DateTime(required=True)
    interview_type = fields.Str(required=True)
    interview_link = fields.Str()

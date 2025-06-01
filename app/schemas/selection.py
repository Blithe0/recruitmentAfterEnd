from marshmallow import Schema, fields, post_load
from app.models.selection import Selection
import json

class SelectionSchema(Schema):
    selection_id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    steps = fields.List(fields.Dict(), required=True)

    @post_load
    def make_selection(self, data, **kwargs):
        steps_json = json.dumps(data.pop('steps'))
        return Selection(**data, steps_json=steps_json)

    def dump(self, obj, **kwargs):
        result = super().dump(obj, **kwargs)
        result['steps'] = json.loads(obj.steps_json)
        return result

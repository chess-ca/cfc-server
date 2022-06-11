
import dataclasses, datetime, uuid, json
from json import *

_has_pydantic = False
try:
    import pydantic
    _has_pydantic = True
except ImportError as e:
    pass


class JSONEncoderPlus(json.JSONEncoder):
    """
    A JSON Encoder that converts a few more types of objects:
    - dataclasses, Pydantic models
    - datetime, date, time, UUID,
    - flask.Markup (having __html__ method)
    - Flask usage: `from codeboy4py.py.json import JSONEncoderPlus`
      and set `flask_app.json_encoder=JSONEncoderPlus`
    - Other usage: `from codeboy4py.py import json` and then
      `json.dumps`, json.dump`, etc.
    """
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if _has_pydantic and isinstance(obj, pydantic.BaseModel):
            return obj.dict()
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time,)):
            return obj.isoformat()
        if hasattr(obj, '__html__'):    # includes flask.Markup
            return obj.__html__()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


def dump(obj, **kwargs):
    kwargs['cls'] = JSONEncoderPlus
    return json.dump(obj, **kwargs)


def dumps(obj, **kwargs):
    kwargs['cls'] = JSONEncoderPlus
    return json.dumps(obj, **kwargs)


import dataclasses, datetime, uuid, json

try:
    import pydantic
    has_pydantic = True
except ImportError as e:
    has_pydantic = False


class JSONEncoderPlus(json.JSONEncoder):
    """
    A JSON Encoder that converts a few more types of objects:
    Python dataclasses, Pydantic models, datetime, date, time, UUID,
    flask.Markup (having __html__ method)
    - To use, `from codeboy4py.py.json import JSONEncoderPlus`
      and set `flask_app.json_encoder=JSONEncoderPlus`
    """
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if has_pydantic and isinstance(obj, pydantic.BaseModel):
            return obj.dict()
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time,)):
            return obj.isoformat()
        if hasattr(obj, '__html__'):    # includes flask.Markup
            return obj.__html__()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

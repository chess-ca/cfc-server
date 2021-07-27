"""
codeboy4py.py.pydantic
- Everything the pydantic package has plus some goodies.
- App code can import this instead of the real pydantic package.
"""
from pydantic import *


class BaseModelPlus(BaseModel):
    _cb4py_pydantic_errors: list

    @classmethod
    def new(cls, attrs: dict):
        instance, errors = None, []
        try:
            instance = cls(**attrs)
        except ValidationError as e:
            errors = e.errors()
        return instance, errors


def simplify_errors(pydantic_errors):
    e_list = []
    for e in pydantic_errors:
        e_list.append(dict(
            attr=', '.join(e['loc']),
            emsg=e['msg'] if len(e['loc']) != 1
                else e['msg'].replace('value', f'"{e["loc"][0]}"', 1),
            etype=e['type'],
        ))
    return e_list

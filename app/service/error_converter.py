from pydantic import ValidationError


def convert_errors(e: ValidationError):
    response = {}
    for error in e.errors():
        if 'loc' not in error or 'msg' not in error:
            continue
        field = ".".join(error['loc']) if isinstance(error['loc'], tuple) else error['loc']
        response[field] = error['msg'].capitalize()
    return response

from fastapi import Request


def get_headers(request: Request):
    headers = dict(request.headers)
    if 'authorization' in headers:
        del headers['authorization']
    if 'cookie' in headers:
        del headers['cookie']
    return headers

import json
import os
from typing import Optional

import requests
from dotenv import load_dotenv

from tracardi.config import tracardi
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session, SessionMetadata
from tracardi.service.string_manager import remove_non_alpha

load_dotenv()


def get_tenant_name_from_host(hostname) -> Optional[str]:
    parts = hostname.split(".")
    if len(parts) >= 3:
        _tenant_candidate = remove_non_alpha(parts[0])
        if len(_tenant_candidate) >= 3 and not _tenant_candidate.isnumeric():
            return _tenant_candidate
    return None


def get_test_tenant():
    if not tracardi.multi_tenant:
        tenant = tracardi.version.name
    else:
        host = os.environ.get('HOST', None)
        if host is None:
            raise ValueError("Can not find HOST env. Set HOST for multi-tenant testing.")

        parts = host.split("//")
        if len(parts) > 1:
            host = parts[1].strip(":")
        tenant = get_tenant_name_from_host(host)

    if tenant is None:
        raise ValueError("Can not find tenant in HOST.")

    return tenant


class Endpoint:

    def __init__(self, auth=True):
        if auth:
            self.token = self.auth()
        else:
            self.token = ""

    @staticmethod
    def host(path):
        return "{}:{}{}".format(os.environ['HOST'], os.environ['PORT'], path)

    def set_credentials(self, username: str = None, password: str = None):
        self.token = self.auth(username, password)

    def auth(self, username: str = None, password: str = None):
        response = requests.post(self.host('/user/token'),
                                 {"username": os.environ['LOGIN'] if username is None else username,
                                  "password": os.environ['PASS'] if password is None else password}
                                 )

        data = response.json()
        if response.status_code == 200:
            return "{} {}".format(data['token_type'], data['access_token'])
        else:
            raise ConnectionError(f"Tracardi connection error status {response.status_code}. Details: {data}")

    def request(self, endpoint, data=None, params=None, method='POST'):
        return requests.request(
            method,
            self.host(endpoint),
            data=data,
            params=params,
            timeout=180,
            headers={"Authorization": self.token})

    def post(self, endpoint, data=None):
        return self.request(endpoint, json.dumps(data), method="post")

    def get(self, endpoint, params=None):
        return self.request(endpoint, params=params, method="get")

    def delete(self, endpoint, data=None, params=None):
        return self.request(endpoint, json.dumps(data), params=params, method="delete")

    def put(self, endpoint, data=None, params=None):
        return self.request(endpoint, json.dumps(data), params=params, method="put")

    def set_token(self, token: str):
        self.token = token


def create_session(session_id, profile_id=None):
    if profile_id is not None:
        session = Session(id=session_id, profile=Profile(id=profile_id), metadata=SessionMetadata())
    else:
        session = Session(id=session_id, metadata=SessionMetadata())

    session = json.loads(session.json())

    endpoint = Endpoint()
    response = endpoint.post("/sessions/import", data=[session])
    result = response.json()
    assert response.status_code == 200
    assert result['saved'] == 1
    assert endpoint.get("/sessions/refresh").status_code == 200

    return result


def create_profile(profile_id):
    endpoint = Endpoint()
    response = endpoint.post('/profiles/import', data=[{"id": profile_id}])
    result = response.json()
    assert result["saved"] == 1
    assert response.status_code == 200

    assert endpoint.get("/profiles/refresh").status_code == 200


def get_session(session_id):
    endpoint = Endpoint()
    return endpoint.get(f'/session/{session_id}')


def get_profile(session_id):
    endpoint = Endpoint()
    return endpoint.get(f'/profile/{session_id}')

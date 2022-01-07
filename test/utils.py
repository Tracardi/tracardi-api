import asyncio
import json
import os
import requests
from dotenv import load_dotenv

from tracardi.domain.profile import Profile
from tracardi.domain.session import Session, SessionMetadata
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor

load_dotenv()


class Endpoint:

    def __init__(self):
        self.token = self.auth()

    @staticmethod
    def host(path):
        return "{}:{}{}".format(os.environ['HOST'], os.environ['PORT'], path)

    def auth(self):
        response = requests.post(self.host('/token'),
                                 {"username": os.environ['LOGIN'], "password": os.environ['PASS']})
        data = response.json()
        return "{} {}".format(data['token_type'], data['access_token'])

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


async def create_session(session_id, profile_id=None):
    if profile_id is not None:
        session = Session(id=session_id, profile=Profile(id=profile_id), metadata=SessionMetadata())
    else:
        session = Session(id=session_id, metadata=SessionMetadata())

    result = await StorageFor(session).index().save()
    assert result.saved == 1
    await storage.driver.session.refresh()
    return result


def run_new_event_loop(func, **kwargs):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func(**kwargs))
    loop.close()

import logging
import os
from typing import Optional

import grpc
from app.api.proto.stubs import pro_services_pb2 as pb2, pro_services_pb2_grpc as pb2_grpc
from google.protobuf import json_format

from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.pro.auth import get_tpro_token

_local_path = os.path.dirname(__file__)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

with open(os.path.join(_local_path, 'certs/server.crt'), 'rb') as f:
    trusted_certs = f.read()
credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)


class TracardiProClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self, host, port=50000, secure=False):
        self.host = host
        self.server_port = port

        host = '{}:{}'.format(self.host, self.server_port)
        logger.info(f"Tracardi PRO set to {host}")
        if secure:
            self.channel = grpc.secure_channel(host, credentials)
        else:
            self.channel = grpc.insecure_channel(host)

        # bind the client and the server
        self.stub = pb2_grpc.ServiceStub(self.channel)

    def validate(self, token) -> Optional[str]:
        try:
            message = pb2.EmptyParams()
            response = self.stub.validate(message, metadata=[('token', token)])
            return response.token if response.token != "" else None
        except grpc.RpcError as e:
            return None

    def sign_in(self, username, password) -> tuple:
        try:
            response = self.stub.sign_in(pb2.Credentials(username=username, password=password))
            return response.token, response.host
        except grpc.RpcError as e:
            raise PermissionError(e.details())

    async def get_available_services(self, query="", category=""):
        message = pb2.ServiceQuery(query=query, category=category, version=tracardi.version.version)

        services = self.stub.get_available_services(message, metadata=[('token', await get_tpro_token())])
        return json_format.MessageToDict(services)

    async def get_plugin(self, module):
        message = pb2.PluginMetaData(module=module)
        services = self.stub.get_plugin(message, metadata=[('token', await get_tpro_token())])
        return json_format.MessageToDict(services)

    def sign_up(self, username, password):
        response = self.stub.sign_up(pb2.Credentials(username=username, password=password))
        return response.token

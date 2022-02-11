import os
from typing import Optional

import grpc
from app.api.proto.stubs import pro_services_pb2 as pb2, pro_services_pb2_grpc as pb2_grpc
from google.protobuf import json_format

_local_path = os.path.dirname(__file__)

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
        self.token = None

        host = '{}:{}'.format(self.host, self.server_port)
        if secure:
            self.channel = grpc.secure_channel(host, credentials)
        else:
            self.channel = grpc.insecure_channel(host)

        # bind the client and the server
        self.stub = pb2_grpc.ServiceStub(self.channel)

    def save_token(self, token):
        self.token = token

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

    def get_available_services(self):
        message = pb2.EmptyParams()
        services = self.stub.get_available_services(message, metadata=[('token', self.token)])
        return json_format.MessageToDict(services)

    def get_available_hosts(self):
        message = pb2.EmptyParams()
        hosts = self.stub.get_available_hosts(message, metadata=[('token', self.token)])
        return json_format.MessageToDict(hosts)

    def sign_up(self, username, password):
        response = self.stub.sign_up(pb2.Credentials(username=username, password=password))
        return response.token

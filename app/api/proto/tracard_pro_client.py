import os
from typing import Optional

import grpc
from app.api.proto.stubs import tracardi_pro_services_pb2 as pb2, tracardi_pro_services_pb2_grpc as pb2_grpc
from google.protobuf import json_format

_local_path = os.path.dirname(__file__)

with open(os.path.join(_local_path,'certs/server.crt'), 'rb') as f:
    trusted_certs = f.read()
credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)


class TracardiProClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.server_port = port
        self.token = None

        # instantiate a secure channel
        self.channel = grpc.secure_channel('{}:{}'.format(self.host, self.server_port), credentials)

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

    def sign_in(self, username, password) -> str:
        try:
            response = self.stub.sign_in(pb2.Credentials(username=username, password=password))
            return response.token
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


if __name__ == '__main__':
    import sys
    sys.path.append(os.path.dirname(__file__) + "/stubs")

    print(sys.path)
    client = TracardiProClient()
    # r = client.authorize("a", "b")
    # print(r)
    result = client.get_available_hosts()
    print(f'{result}')

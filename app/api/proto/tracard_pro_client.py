import os

import grpc
import tracardi_pro_services_pb2_grpc as pb2_grpc
import tracardi_pro_services_pb2 as pb2

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

    def authorize(self, username, password):
        try:
            response = self.stub.authorize(pb2.Credentials(username=username, password=password))
            self.save_token(response.token)
            return True
        except grpc.RpcError as e:
            # ouch!
            # lets print the gRPC error message
            # which is "Length of `Name` cannot be more than 10 characters"
            print(e.details())
            # lets access the error code, which is `INVALID_ARGUMENT`
            # `type` of `status_code` is `grpc.StatusCode`
            status_code = e.code()
            # should print `INVALID_ARGUMENT`
            print(status_code.name)
            # should print `(3, 'invalid argument')`
            print(status_code.value)
            return False

    def get_available_services(self):
        message = pb2.EmptyParams()
        return self.stub.get_available_services(message, metadata=[('token', self.token)])


if __name__ == '__main__':
    client = TracardiProClient()
    # r = client.authorize("a", "b")
    # print(r)
    result = client.get_available_services()
    print(f'{result}')

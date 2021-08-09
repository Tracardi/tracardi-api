import os


class AuthConfig:
    def __init__(self, env):
        self.user = env['USER_NAME'] if 'USER_NAME' in env else 'admin'
        self.password = env['PASSWORD'] if 'PASSWORD' in env else 'admin'


auth = AuthConfig(os.environ)

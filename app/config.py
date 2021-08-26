import os


class AuthConfig:
    def __init__(self, env):
        self.user = env['USER_NAME'] if 'USER_NAME' in env else 'admin'
        self.password = env['PASSWORD'] if 'PASSWORD' in env else 'admin'


class ServerConfig:
    def __init__(self, env):
        self.update_plugins_on_start_up = env['UPDATE_PLUGINS_ON_STARTUP'] if 'UPDATE_PLUGINS_ON_STARTUP' in env else False


auth = AuthConfig(os.environ)
server = ServerConfig(os.environ)

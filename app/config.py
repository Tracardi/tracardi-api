import os


class AuthConfig:
    def __init__(self, env):
        self.user = env['USER_NAME'] if 'USER_NAME' in env else 'admin'
        self.password = env['PASSWORD'] if 'PASSWORD' in env else 'admin'


class ServerConfig:
    def __init__(self, env):
        self.update_plugins_on_start_up = env['UPDATE_PLUGINS_ON_STARTUP'] if 'UPDATE_PLUGINS_ON_STARTUP' in env else True
        self.make_slower_responses = float(env['DEBUG_MAKE_SLOWER_RESPONSES']) if 'DEBUG_MAKE_SLOWER_RESPONSES' in env else 0
        self.heartbeat_every = env['RUN_HEARTBEAT_EVERY'] if 'RUN_HEARTBEAT_EVERY' in env else 5*60
        self.tasks_every = env['RUN_TASKS_EVERY'] if 'RUN_TASKS_EVERY' in env else 1
        self.page_size = int(env['AUTOLOAD_PAGE_SIZE']) if 'AUTOLOAD_PAGE_SIZE' in env else 25


auth = AuthConfig(os.environ)
server = ServerConfig(os.environ)

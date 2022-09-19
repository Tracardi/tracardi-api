import os


class ServerConfig:
    def __init__(self, env):
        self.update_plugins_on_start_up = env[
            'UPDATE_PLUGINS_ON_STARTUP'] if 'UPDATE_PLUGINS_ON_STARTUP' in env else True
        self.make_slower_responses = float(
            env['DEBUG_MAKE_SLOWER_RESPONSES']) if 'DEBUG_MAKE_SLOWER_RESPONSES' in env else 0
        self.heartbeat_every = env['RUN_HEARTBEAT_EVERY'] if 'RUN_HEARTBEAT_EVERY' in env else 5 * 60
        self.tasks_every = env['RUN_TASKS_EVERY'] if 'RUN_TASKS_EVERY' in env else 1
        self.page_size = int(env['AUTOLOAD_PAGE_SIZE']) if 'AUTOLOAD_PAGE_SIZE' in env else 25
        self.expose_gui_api = (env['EXPOSE_GUI_API'].lower() == "yes") if 'EXPOSE_GUI_API' in env else True
        self.x_forwarded_ip_header = env['USE_X_FORWARDED_IP'] if 'USE_X_FORWARDED_IP' in env else None
        self.api_docs = (env['API_DOCS'].lower() == "yes") if 'API_DOCS' in env else True


server = ServerConfig(os.environ)

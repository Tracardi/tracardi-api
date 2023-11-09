import os


class ServerConfig:
    def __init__(self, env):
        self.make_slower_responses = float(
            env['DEBUG_MAKE_SLOWER_RESPONSES']) if 'DEBUG_MAKE_SLOWER_RESPONSES' in env else 0
        self.page_size = int(env['AUTOLOAD_PAGE_SIZE']) if 'AUTOLOAD_PAGE_SIZE' in env else 25
        self.x_forwarded_ip_header = env.get('USE_X_FORWARDED_IP', None)
        self.api_docs = (env['API_DOCS'].lower() == "yes") if 'API_DOCS' in env else True
        self.performance_tracking = env.get('PERFORMANCE_TRACKING', 'yes').lower() == "yes"


server = ServerConfig(os.environ)

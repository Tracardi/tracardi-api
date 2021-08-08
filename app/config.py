import os


class TracardiConfig:
    def __init__(self, env):
        self.user = env['USER_NAME'] if 'USER_NAME' in env else 'admin'
        self.password = env['PASSWORD'] if 'PASSWORD' in env else 'admin'
        self.track_debug = env['TRACK_DEBUG'] if 'TRACK_DEBUG' in env else False


tracardi = TracardiConfig(os.environ)

import argparse
import os
import time
from tornado.log import app_log
from tornado.ioloop import IOLoop
from tornado.web import Application
from urllib.parse import urlparse
from jhub_spawner_permissions.state import Settings
from jhub_spawner_permissions.handlers import default_handlers
from jhub_spawner_permissions.util import init_jinja_env, get_template_paths


class SpawnerPermissionApp():

    handlers = []

    def __init__(self):
        self.handlers.extend(default_handlers)

    # Create application
    def start(self, port=5000, address='127.0.0.1', **kwargs):
        settings = Settings.get_settings()
        application = Application(self.handlers, **settings)
        application.listen(port, address)
        IOLoop.current().start()


def main():
    args = parse_arguments()
    app = SpawnerPermissionApp()
    app.start(**vars(args))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--address',
        '-a',
        default='127.0.0.1',
        type=str
    )
    parser.add_argument(
        '--port',
        '-p',
        default=5000,
        help="port for the spawner permissions to listen on",
        type=int
    )
    return parser.parse_args()

if __name__ == "__main__":
    main()

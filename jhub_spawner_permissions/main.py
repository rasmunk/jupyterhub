import os
import time
from tornado.log import app_log
from tornado.ioloop import IOLoop
from tornado.web import Application
from urllib.parse import urlparse
from jhub_spawner_permissions.handlers import default_handlers
from jhub_spawner_permissions.util import init_jinja


def init_settings():
    settings = {}

    jinja2_env = init_jinja()
    if jinja2_env:
        settings['jinja2_env'] = jinja2_env


class SpawnerPermissionApp():

    handlers = []

    def init_handlers(self):
        self.handlers.extend(default_handlers)

    # Create application
    def start(self):
        application = Application(self.handlers)
        url = urlparse(os.environ.get('JUPYTERHUB_SERVICE_URL'))
        application.listen(url.port, url.hostname)
        IOLoop.current().start()


if __name__ == "__main__":
    app = SpawnerPermissionApp()
    app.init_handlers()

    settings = init_settings()

    # Check if JupyterHub is running
    app.start()

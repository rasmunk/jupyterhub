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

    def init_handlers(self):
        self.handlers.extend(default_handlers)

    # Create application
    def start(self):
        settings = Settings.get_settings()
        application = Application(self.handlers, **settings)
        url = urlparse(os.environ.get('JUPYTERHUB_SERVICE_URL'))
        application.listen(url.port, url.hostname)
        IOLoop.current().start()


if __name__ == "__main__":
    app = SpawnerPermissionApp()
    app.init_handlers()

    # Check if JupyterHub is running
    app.start()

import os
import json
from tornado import web
from tornado import escape
from tornado.log import app_log
from jupyterhub.services.auth import HubAuthenticated


# Get JupyterHub url prefix from env
# https://jupyterhub.readthedocs.io/en/stable/reference/services.html
prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')


class SpawnerPermissionHandler(HubAuthenticated, web.RequestHandler):

    @web.authenticated
    async def get(self):
        app_log.info("Get spawner permissions")
        # user = self.get_current_user()
        self.render('templates/permissions.html')

    def write_to_json(self, doc):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))


default_handlers = [
    (prefix + '/?', SpawnerPermissionHandler),
    (r'.*', SpawnerPermissionHandler)
]

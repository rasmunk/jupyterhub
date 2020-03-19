import os
import json
from tornado import web
from tornado import escape
from tornado.log import app_log
from jupyterhub.app import JupyterHub
from jupyterhub.services.auth import HubAuthenticated
from jhub_spawner_permissions.orm import User
from jhub_spawner_permissions.state import Settings

# Get JupyterHub url prefix from env
# https://jupyterhub.readthedocs.io/en/stable/reference/services.html
prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')


class BaseHandler(HubAuthenticated, web.RequestHandler):

    @property
    def db(self):
        return self.settings['db']

    def template_namespace(self):
        # Minimum required fields by page.html
        ns = dict(
            base_url=JupyterHub.base_url,
            prefix=JupyterHub.base_url)
        return ns

    def render_template(self, name, **ns):
        settings = Settings.get_settings()
        template_ns = {}
        template_ns.update(ns)

        template = settings['jinja2_env'].get_template(name)
        return template.render(**template_ns)

class SpawnerPermissionHandler(BaseHandler):

    # TODO, base of JupyterHub base template (page.html)
    # Must be admin
    # @web.authenticated
    async def get(self):
        users = User.all(self.db)
        html = self.render_template('users.html', users=users)
        self.finish(html)

class UserPermissionHandler(BaseHandler):

    async def get(self, user_id):
        user = User.find(user_id, self.db)
        html = self.render_template('user.html', user=user)
        self.finish(html)

default_handlers = [
    (prefix + '/?', SpawnerPermissionHandler),
    (r'.*', SpawnerPermissionHandler)
]

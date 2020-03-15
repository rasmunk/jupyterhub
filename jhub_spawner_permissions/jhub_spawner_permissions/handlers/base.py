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


def template_namespace():
    # Minimum required fields by page.html
    ns = dict(
        base_url=JupyterHub.base_url,
        prefix=JupyterHub.base_url,
        user=None)
    return ns


def render_template(name, **ns):
    settings = Settings.get_settings()
    template_ns = {}
    template = settings['jinja2_env'].get_template(name)
    return template.render(**template_ns)


class BaseHandler(HubAuthenticated, web.RequestHandler):

    @property
    def db(self):
        return self.db


class SpawnerPermissionHandler(BaseHandler):

    # TODO, base of JupyterHub base template (page.html)
    # Must be admin
    # @web.authenticated
    async def get(self):
        users = User.all(self.db)
        self.render('users.html', users=users)

    # # TODO, take user 
    # @web.authenticated
    # async def post(self):
    #     pass

    

class UserPermissionHandler(BaseHandler):

    async def get(self, user_id):
        user = User.find(user_id, self.db)
        self.render('user', user=user)


default_handlers = [
    (prefix + '/?', SpawnerPermissionHandler),
    (r'.*', SpawnerPermissionHandler)
]

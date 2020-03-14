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
    # template_ns.update(ns)
    template = settings['jinja2_env'].get_template(name)
    return template.render(**template_ns)


class SpawnerPermissionHandler(HubAuthenticated, web.RequestHandler):

    # TODO, base of JupyterHub base template (page.html)
    # Must be admin
#    @web.authenticated
    async def get(self):
        app_log.info("Get spawner permissions")
        namespace = {'user': self.get_current_user()}
        self.render('permissions.html')
        # render_template('permissions.html', **namespace)

    # TODO, take user 
    @web.authenticated
    async def post(self):
        pass


default_handlers = [
    (prefix + '/?', SpawnerPermissionHandler),
    (r'.*', SpawnerPermissionHandler)
]

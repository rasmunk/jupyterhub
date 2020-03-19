import sys
from jhub_spawner_permissions.jhub_spawner_permissions.manager import spawn_allowed

c = get_config()

c.JupyterHub.ip = '127.0.0.1'
# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '172.17.0.1'
c.JupyterHub.port = 8080

c.JupyterHub.debug = True

c.JupyterHub.authenticator_class = 'jhubauthenticators.DummyAuthenticator'
c.DummyAuthenticator.password = 'password'

c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
c.SystemUserSpawner.image = 'jupyter/base-notebook'

c.SystemUserSpawner.container_port = 8888
c.SystemUserSpawner.container_spec = {
    'env': {'JUPYTER_LAB_ENABLE': '1'}
}

# c.SystemUserSpawner.pre_spawn_hook = spawn_allowed

c.JupyterHub.services = [{
    'name': 'jhub_spawner_permissions',
    'url': 'http://127.0.0.1:5000',
    'command': [sys.executable, '/home/rasmus/repos/jupyterhub/jhub_spawner_permissions/main.py']}
]
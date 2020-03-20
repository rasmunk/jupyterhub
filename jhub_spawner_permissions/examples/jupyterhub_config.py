#from jhub_spawner_permissions import spawn_allowed
c = get_config()
c.JupyterHub.ip = '127.0.0.1'

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '127.0.0.1'
c.JupyterHub.port = 8080

c.JupyterHub.authenticator_class = 'jhubauthenticators.DummyAuthenticator'
c.DummyAuthenticator.password = 'password'

c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'
c.SimpleLocalProcessSpawner.container_spec = {
    'env': {'JUPYTER_ENABLE_LAB': '1'}
}



#c.SimpleLocalProcessSpawner.pre_spawn_hook = spawn_allowed

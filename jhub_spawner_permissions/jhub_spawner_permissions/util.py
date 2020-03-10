import os
from jinja2.loaders import ChoiceLoader, PrefixLoader, FileSystemLoader
from jinja2.environment import Environment
from jupyterhub._data import get_data_files

# Use JupyterHub to find its templates
DATA_FILES_PATH = get_data_files()
global_templates_dir = os.path.join(DATA_FILES_PATH, 'templates')
permissions_templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

def get_template_paths():
    return [global_templates_dir, permissions_templates_dir]

def init_jinja_env():
    template_paths = get_template_paths()
    loader = ChoiceLoader(
        [
            PrefixLoader({'templates': FileSystemLoader([template_paths[0]])}, '/'),
            FileSystemLoader(template_paths)
        ]
    )
    return Environment(loader=loader)

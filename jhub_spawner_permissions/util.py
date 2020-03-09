import os
from jinja2.loaders import ChoiceLoader, PrefixLoader, FileSystemLoader
from jinja2.environment import Environment
from jupyterhub._data import get_data_files


# Use JupyterHub to find its templates
DATA_FILES_PATH = get_data_files()
templates_dir = os.path.join(DATA_FILES_PATH, 'templates')


def init_jinja():
    base_paths = [templates_dir]
    loader = ChoiceLoader(
        [
            PrefixLoader({'templates': FileSystemLoader(base_paths)}, '/'),
            FileSystemLoader(base_paths)
        ]
    )
    return Environment(loader=loader)

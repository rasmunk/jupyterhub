import os
from . import base

default_handlers = []
for mod in (base,):
    default_handlers.extend(mod.default_handlers)


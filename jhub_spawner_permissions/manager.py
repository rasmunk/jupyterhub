from tornado import gen
from .orm import User
from .orm import DBConnectionManager


@gen.coroutine
def spawn_allowed(spawner):
    db_manager = DBConnectionManager()
    user = User.find(db_manager.db, spawner.user.name)
    if not user:
        user = User(name=spawner.user.name)
        db_manager.add(user)
        db_manager.commit()

    if hasattr(spawner, 'image'):
        image = spawner.image
        if image not in user.images:
            raise PermissionError("You don't have permission to spawn {}"
                                  .format(image))

    return True

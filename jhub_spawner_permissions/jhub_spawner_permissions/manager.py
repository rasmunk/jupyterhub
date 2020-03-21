from tornado import gen
from traitlets.config import LoggingConfigurable
from .orm import User, Image, Permission, UserImagePermissions
from .orm import DBConnectionManager
from .error import NotAllowedError, SetupPermissionError, SetupUserError, SetupImageError

PACKAGE_NAME = "SpawnerPermissions"

@gen.coroutine
def create_user_hook(authenticator, handler, authentication):
    """ Creates the authenticated user in ther permissions DB """

    name = authentication['name']
    db_manager = DBConnectionManager()
    user = User.find(db_manager.db, first=True, name=name)
    if not user:
        user = User(name=name)
        db_manager.add(user)
        if not db_manager.commit():
            db_manager.close()
            raise SetupUserError("Failed to setup the your user "
                                 "account: {} in the {} DB"
                                 .format(name, PACKAGE_NAME))
        db_manager.close()
    return authentication


@gen.coroutine
def permission_spawn_hook(spawner):
    """ Primary pre_spawn_hook for authenticating the spawn """

    logger = spawner.log
    username = spawner.user.name
    image = yield get_spawner_image(spawner)
    if not image:
        logger.error("{} - a valid image was "
                     "not provided by the spawner".format(PACKAGE_NAME))
        return False

    db_manager = DBConnectionManager()
    prepared = yield prepare_image(db_manager, image)
    if not prepared:
        raise SetupImageError("Failed to setup the image: {} in the {} DB"
                              .format(image, PACKAGE_NAME))

    db_user = User.find(db_manager.db, first=True, name=username)
    if not db_user:
        # Ensure that the authenticator calls `create_user_hook`
        # upon a successfull login to create the user in the DB
        logger.error("{} - the provided user {} doesn't exist in the db"
                     .format(PACKAGE_NAME, username))
        raise SetupPermissionError("Your user account: {} doesn't exist "
                                   "in the database, please try and reauthenticate"
                                   .format(username))

    # Find permissions for that particular user
    db_image = Image.find(db_manager.db, first=True, name=image)
    uid = UserImagePermissions.find(db_manager.db, first=True,
                                    user=db_user, image=db_image)
    if not uid:
        # The default permission is allowed
        db_permission = Permission.find(db_manager.db, first=True,
                                        allowed=True)
        if not db_permission:
            # Create new permission with `allowed=True`
            db_permission = Permission(allowed=True)
            db_manager.add(db_permission)
            if not db_manager.commit():
                logger.error("{} - failed to add Permission: {}".format(PACKAGE_NAME,
                db_permission))
                raise SetupPermissionError("Failed to setup your permissions")

        uid = UserImagePermissions(user=db_user, image=db_image,
                                   permission=db_permission)
        db_manager.add(uid)
        if not db_manager.commit():
            logger.error("{} - failed to add UserImagePermission: {}".format(PACKAGE_NAME,
            uid))
            raise SetupPermissionError("Failed to setup your permissions")
    
    if not uid.permission.allowed:
        logger.info("{} - user {} tried to spawn {} without permission".format(
            PACKAGE_NAME, username, image
        ))
        raise NotAllowedError("You don't have permission to spawn {}"
                                .format(image))
    return True


@gen.coroutine
def get_spawner_image(spawner):
    """ Validates that the spawner provides a selected image to validate
    permissions against """

    logger = spawner.log
    logger.info("{} - validating spawner".format(PACKAGE_NAME))
    # So far the convention seems to be that the spawner image attribute
    # is defined as `image`
    if hasattr(spawner, 'image'):
        image = getattr(spawner, 'image')
        if isinstance(image, str):
            return image
    return False


# Register spawner images
@gen.coroutine
def prepare_image(db_manager, image):
    """ """

    db_image = Image.find(db_manager.db, first=True, name=image)
    if not db_image:
        # Save the image to the DB
        new_image = Image(name=image)
        db_manager.add(new_image)
        if not db_manager.commit():
            return False
    return True

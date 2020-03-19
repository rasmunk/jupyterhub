from jhub_spawner_permissions.util import init_jinja_env, get_template_paths, new_db_manager


class Settings:

    @staticmethod
    def get_settings():
        template_paths = get_template_paths()[1]
        db = new_db_manager()

        settings = dict(
            db=db.db,
            template_path=template_paths,
        )

        jinja2_env = init_jinja_env()
        if jinja2_env:
            settings['jinja2_env'] = jinja2_env
        return settings

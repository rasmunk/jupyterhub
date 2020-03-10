from jhub_spawner_permissions.state import settings

class RenderEngine:

    @staticmethod
    def render_template(name):
        template = settings['jinja2_env'].get_template(name)
        return template.render(**{})

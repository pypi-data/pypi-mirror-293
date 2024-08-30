from jinja2 import (
    Environment,
    PackageLoader,
    select_autoescape,
    Template,
    TemplateError,
    TemplateNotFound,
    TemplateRuntimeError,
)


def get_local_template() -> Template:
    template_name = "sonarcloud_report.j2"
    try:
        env = Environment(
            loader=PackageLoader("sonarcloud_report", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,  # Removes unnecessary spaces before and after blocks and loop
            lstrip_blocks=True,  # Removes unnecessary spaces before blocks and loop
        )
        return env.get_template(template_name)
    except TemplateNotFound as e:
        raise TemplateError(f"Template not found: {template_name}") from e
    except TemplateRuntimeError as e:
        raise TemplateError(f"Template runtime error: {template_name}") from e
    except Exception as e:
        raise TemplateError(f"Template error: {template_name}") from e

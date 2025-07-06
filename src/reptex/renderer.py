from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader


def create_jinja_env(template_dir: Path) -> Environment:
    """
    Create a configured Jinja2 environment for rendering LaTeX templates.

    Args:
        template_dir: Directory containing Jinja2 templates.

    Returns:
        Configured Jinja2 Environment.
    """
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
        autoescape=False,
    )


def render_template(template_path: Path, context: Dict[str, Any]) -> str:
    """
    Render a Jinja2 template file with the given context.

    Args:
        template_path: Path to the template file (.tex.j2).
        context: Dictionary of variables to substitute into the template.

    Returns:
        Rendered template as a string.
    """
    template_dir = template_path.parent
    template_name = template_path.name

    env = create_jinja_env(template_dir)
    template = env.get_template(template_name)
    return template.render(**context)

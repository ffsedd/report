import logging
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateNotFound,
    TemplateSyntaxError,
)

from reptex.sections import Section

logger = logging.getLogger("reptex")


def create_jinja_env(template_dir: Path) -> Environment:
    """
    Create and configure a Jinja2 Environment for template rendering.

    Args:
        template_dir: Directory where Jinja2 templates are located.

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


def render_template(template_path: Path, context: Dict[str, Any], template_dir: Path) -> str:
    """
    Render a single Jinja2 template with a given context.

    Args:
        template_path: Full path to the template file.
        context: Dictionary of context variables for rendering.
        template_dir: Root directory of all templates.

    Returns:
        Rendered template as a string.

    Raises:
        FileNotFoundError: If the template file does not exist.
        RuntimeError: If there's a syntax error in the template.
    """
    logger.debug(f"Rendering template: {template_path}")
    preview_context = {
        k: (str(v)[:100] + "..." if len(str(v)) > 100 else str(v))
        for k, v in list(context.items())[:5]
    }
    logger.debug(f"Context preview: {preview_context}")

    # Non-template files (e.g. plain TeX or other includes)
    if template_path.suffix != ".j2":
        logger.debug(f"Reading non-template file: {template_path}")
        content = template_path.read_text(encoding="utf-8")
        logger.debug(f"Read {len(content)} characters from file")
        return content

    env = create_jinja_env(template_dir)

    try:
        template = env.get_template(template_path.name)
        rendered = template.render(**context)
        logger.debug(f"Rendered template length: {len(rendered)} characters")
        return rendered
    except TemplateNotFound as err:
        logger.error(f"Template not found: {template_path}", exc_info=True)
        raise FileNotFoundError(f"Template not found: {template_path}") from err
    except TemplateSyntaxError as err:
        logger.error(
            f"Syntax error in template {template_path} at line {err.lineno}: {err.message}",
            exc_info=True,
        )
        raise RuntimeError(
            f"Syntax error in template {template_path} at line {err.lineno}: {err.message}"
        ) from err


def render_templates(
    sections: List[Section], template_dir: Path, layout_template: str = "main.tex.j2"
) -> str:
    """
    Render all sections and the main layout template into a final LaTeX string.

    Args:
        sections: List of Section objects with template names and rendering context.
        template_dir: Path to the directory containing templates.
        layout_template: Name of the layout template (default: "main.tex.j2").

    Returns:
        Fully rendered LaTeX document as a string.

    Raises:
        FileNotFoundError: If the layout template does not exist.
        RuntimeError: If any rendering fails.
    """
    logger.info(f"Starting to render {len(sections)} sections from {template_dir}")
    rendered_sections = []

    for i, section in enumerate(sections, start=1):
        section_path = template_dir / section.template
        logger.info(f"[{i}/{len(sections)}] Rendering: {section_path}")
        logger.debug(f"Context keys: {list(section.context.keys())}")

        try:
            rendered = render_template(section_path, section.context, template_dir)
            rendered_sections.append(rendered)
            logger.info(f"[{i}/{len(sections)}] Successfully rendered: {section.template}")
        except Exception as err:
            logger.error(f"Failed to render section {section.template}: {err}", exc_info=True)
            raise

    layout_path = template_dir / layout_template
    if not layout_path.exists():
        logger.error(f"Layout template not found: {layout_path}")
        raise FileNotFoundError(f"Layout template not found: {layout_path}")

    logger.info(f"Rendering layout template: {layout_path}")
    try:
        result = render_template(layout_path, {"sections": rendered_sections}, template_dir)
        logger.info("Layout template rendered successfully")
        return result
    except Exception as err:
        logger.error(f"Failed to render layout template: {err}", exc_info=True)
        raise

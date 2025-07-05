import logging
from pathlib import Path
from typing import Dict, List

from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateNotFound,
    TemplateSyntaxError,
)

from report.sections import Section

logger = logging.getLogger("report")


def create_jinja_env(template_dir: Path) -> Environment:
    """Create a configured Jinja2 Environment."""
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


def render_template(template_path: Path, context: Dict, template_dir: Path) -> str:
    logger.debug(f"Rendering template: {template_path}")
    preview_context = {
        k: (str(v)[:100] + "..." if len(str(v)) > 100 else str(v))
        for k, v in list(context.items())[:5]
    }
    logger.debug(f"Context preview: {preview_context}")

    if template_path.suffix != ".j2":
        logger.debug(f"Non-template file detected. Reading as text: {template_path}")
        content = template_path.read_text(encoding="utf-8")
        logger.debug(f"Read {len(content)} characters from file")
        return content

    env = create_jinja_env(template_dir)

    try:
        template = env.get_template(template_path.name)
        rendered = template.render(**context)
        logger.debug(f"Rendered template length: {len(rendered)} characters")
        return rendered
    except TemplateNotFound as e:
        logger.error(f"Template not found: {template_path}", exc_info=True)
        raise FileNotFoundError(f"Template not found: {template_path}") from e
    except TemplateSyntaxError as e:
        logger.error(
            f"Syntax error in template {template_path} at line {e.lineno}: {e.message}",
            exc_info=True,
        )
        raise RuntimeError(
            f"Syntax error in template {template_path} at line {e.lineno}: {e.message}"
        ) from e


def render_templates(
    sections: List[Section], template_dir: Path, layout_template: str = "report.tex.j2"
) -> str:
    logger.info(f"Starting to render {len(sections)} sections from {template_dir}")

    rendered_sections = []
    total_sections = len(sections)

    for i, section in enumerate(sections, start=1):
        section_path = template_dir / section.template
        logger.info(f"[{i}/{total_sections}] Rendering section template: {section_path}")
        logger.debug(f"Context keys: {list(section.context.keys())}")

        try:
            rendered = render_template(section_path, section.context, template_dir)
            rendered_sections.append(rendered)
            logger.info(f"[{i}/{total_sections}] Successfully rendered: {section.template}")
        except Exception as e:
            logger.error(f"Failed to render section {section.template}: {e}", exc_info=True)
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
    except Exception as e:
        logger.error(f"Failed to render layout template: {e}", exc_info=True)
        raise

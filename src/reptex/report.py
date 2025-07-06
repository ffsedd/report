import logging
from pathlib import Path
from typing import List

from reptex.compiler import compile_latex
from reptex.logger import setup_logger
from reptex.renderer import render_template
from reptex.section import Section


def generate_report(sections: List[Section], pdf_path: Path) -> Path:
    """
    Render LaTeX from sections and compile to PDF.

    Args:
        sections: List of Section objects with templates and context.
        pdf_path: Path to output PDF file.

    Returns:
        Path to the compiled PDF file.
    """
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logger("reptex", level=logging.INFO)

    logger.info(f"Generating report to: {pdf_path}")
    logger.info(f"Rendering {len(sections)} sections...")

    tex_parts = []
    for i, section in enumerate(sections, start=1):
        logger.info(f"[{i}/{len(sections)}] Rendering: {section.template.name}")
        tex_parts.append(render_template(section.template, section.context))

    full_tex = "\n".join(tex_parts)

    logger.info("Compiling LaTeX to PDF...")
    compiled_pdf = compile_latex(full_tex, pdf_path)
    logger.info(f"PDF successfully written to: {compiled_pdf}")

    return compiled_pdf

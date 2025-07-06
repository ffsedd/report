import subprocess
from pathlib import Path

from reptex.compiler import compile_latex
from reptex.config.config import load_config
from reptex.config.logger import setup_logger
from reptex.renderer import render_templates
from reptex.sections import build_sections


def main() -> None:
    """
    Main entry point for generating the PDF report.

    Steps:
        1. Set the working data directory.
        2. Set up logging to both console and a log file.
        3. Load application and report configuration.
        4. Build the list of report sections.
        5. Render LaTeX templates.
        6. Compile the LaTeX code to a PDF.
        7. Open the generated PDF with Evince.
    """
    # Define where the report data and config are stored
    data_dir = Path("/home/m/report1000")

    # Set up logger
    log_file = data_dir / "logs/render.log"
    logger = setup_logger("reptex", log_file=log_file, level=20)

    logger.info(
        f"---------------------------- Report started in {data_dir} ----------------------------"
    )

    # Load configuration from TOML files
    app_config_path = Path(__file__).parent / "config/app_config.toml"
    cfg = load_config(app_config_path, data_dir=data_dir)

    # Build report sections and render the complete LaTeX source
    template_dir = cfg.report.paths.template_dir
    sections = build_sections(cfg)
    full_tex = render_templates(sections, template_dir)

    # Compile LaTeX into a PDF file
    pdf_path = compile_latex(full_tex, cfg.report.paths.output_dir / "report.pdf")

    # Open the resulting PDF with a viewer
    subprocess.Popen(["evince", str(pdf_path)])


if __name__ == "__main__":
    main()

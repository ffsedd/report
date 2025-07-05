import subprocess
from pathlib import Path

from report.config.logger import setup_logger
from report.config_loader import load_config
from report.latex_compiler import compile_latex
from report.sections import build_sections
from report.template_renderer import render_templates


def main():
    data_dir = Path("/home/m/report1000")

    log_file = data_dir / "logs/render.log"
    logger = setup_logger("report", log_file=log_file, level=20)

    logger.info(
        f"---------------------------- Report started in {data_dir} ----------------------------"
    )

    app_config_path = Path(__file__).parent / "config/app_config.toml"
    cfg = load_config(app_config_path, data_dir=data_dir)

    template_dir = cfg.report.paths.template_dir

    sections = build_sections(cfg)

    full_tex = render_templates(sections, template_dir)

    pdf_path = compile_latex(full_tex, cfg.report.paths.output_dir / "report.pdf")

    subprocess.run(["evince", pdf_path], check=False)


if __name__ == "__main__":
    main()

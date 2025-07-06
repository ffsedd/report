import subprocess
from pathlib import Path

from reptex.report import generate_report
from reptex.sections_example import build_sections

if __name__ == "__main__":
    data_dir = Path("/home/m/report1000")
    templates_dir = data_dir / "templates"
    output_pdf = data_dir / "output/report.pdf"

    sections = build_sections(templates_dir)
    compiled_pdf = generate_report(sections, output_pdf)

    subprocess.Popen(["evince", str(compiled_pdf)])

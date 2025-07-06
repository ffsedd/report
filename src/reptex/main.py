import subprocess
from pathlib import Path

from reptex.report import generate_report
from reptex.sections_example import build_sections

if __name__ == "__main__":
    templates_dir = Path(__file__).parent.parent.parent / "examples/templates"
    output_pdf = Path(__file__).parent.parent.parent / "examples/output/report.pdf"

    sections = build_sections(templates_dir)
    compiled_pdf = generate_report(sections, output_pdf)

    subprocess.Popen(["evince", str(compiled_pdf)])

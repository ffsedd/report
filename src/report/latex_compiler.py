import subprocess
from pathlib import Path


def compile_latex(tex_str: str, output_pdf: Path) -> Path:
    tex_path = output_pdf.with_suffix(".tex")
    print(f"Write {tex_path}")
    tex_path.write_text(tex_str)

    subprocess.run(
        ["latexmk", "-xelatex", "-interaction=nonstopmode", "-quiet", tex_path.name],
        cwd=tex_path.parent,
        check=True,
    )
    return output_pdf

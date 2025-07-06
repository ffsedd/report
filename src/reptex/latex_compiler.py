import subprocess
from pathlib import Path
from typing import Union


def compile_latex(tex_str: str, output_pdf: Union[str, Path]) -> Path:
    """
    Compile a LaTeX string to a PDF using `latexmk` and XeLaTeX.

    Args:
        tex_str: The LaTeX source code as a string.
        output_pdf: Path to the desired output PDF file.

    Returns:
        Path to the compiled PDF.

    Raises:
        RuntimeError: If LaTeX compilation fails.
        OSError: If latexmk is not installed.
    """
    output_pdf = Path(output_pdf)
    tex_path = output_pdf.with_suffix(".tex")

    print(f"[compile_latex] Writing LaTeX source to {tex_path}")
    tex_path.write_text(tex_str, encoding="utf-8")

    try:
        subprocess.run(
            ["latexmk", "-xelatex", "-interaction=nonstopmode", "-quiet", tex_path.name],
            cwd=tex_path.parent,
            check=True,
        )
    except FileNotFoundError as err:
        raise OSError(
            "latexmk not found. Please ensure it is installed and in your PATH."
        ) from err
    except subprocess.CalledProcessError as err:
        raise RuntimeError("LaTeX compilation failed.") from err

    return output_pdf

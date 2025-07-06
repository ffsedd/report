import logging
import subprocess
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def compile_latex(tex_str: str, output_pdf: Union[str, Path], latexmk: bool = False) -> Path:
    """
    Compile a LaTeX string to a PDF using XeLaTeX or latexmk with XeLaTeX.

    Args:
        tex_str: The LaTeX source code as a string.
        output_pdf: Path to the desired output PDF file.
        latexmk: If True, use latexmk with -xelatex option; otherwise call xelatex directly.

    Returns:
        Path to the compiled PDF.

    Raises:
        RuntimeError: If LaTeX compilation fails.
        OSError: If required executables are not found.
    """
    output_pdf = Path(output_pdf)
    tex_path = output_pdf.with_suffix(".tex")
    tex_path.write_text(tex_str, encoding="utf-8")
    logger.debug(f"Wrote LaTeX source to {tex_path}")

    cmd = (
        ["latexmk", "-xelatex", "-interaction=nonstopmode", "-quiet", tex_path.name]
        if latexmk
        else [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            tex_path.name,
        ]
    )

    logger.debug(f"Running command: {' '.join(cmd)} in {tex_path.parent}")

    try:
        completed = subprocess.run(
            cmd,
            cwd=tex_path.parent,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        logger.debug(f"LaTeX compilation stdout:\n{completed.stdout}")
        logger.debug(f"LaTeX compilation stderr:\n{completed.stderr}")
    except FileNotFoundError as err:
        executable = cmd[0]
        logger.error(
            f"Executable '{executable}' not found. Make sure it is installed and on PATH."
        )
        raise OSError(
            f"Executable '{executable}' not found. Please ensure it is installed and in your PATH."
        ) from err
    except subprocess.CalledProcessError as err:
        logger.error(f"LaTeX compilation failed (exit {err.returncode}). stdout:\n{err.stdout}")
        logger.error(f"LaTeX compilation stderr:\n{err.stderr}")
        raise RuntimeError(f"LaTeX compilation failed with exit code {err.returncode}") from err

    if not output_pdf.exists():
        logger.error(f"Expected output PDF '{output_pdf}' not found after compilation.")
        raise RuntimeError(f"Expected output PDF '{output_pdf}' not found after compilation.")

    logger.info(f"Successfully compiled PDF: {output_pdf}")
    return output_pdf

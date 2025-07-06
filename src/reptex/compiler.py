import subprocess
from pathlib import Path
from typing import Union


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

    print(f"[compile_latex] Writing LaTeX source to {tex_path}")
    tex_path.write_text(tex_str, encoding="utf-8")

    if latexmk:
        cmd = ["latexmk", "-xelatex", "-interaction=nonstopmode", "-quiet", tex_path.name]
    else:
        cmd = [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            tex_path.name,
        ]

    try:
        subprocess.run(
            cmd,
            cwd=tex_path.parent,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
    except FileNotFoundError as err:
        executable = cmd[0]
        raise OSError(
            f"Executable '{executable}' not found. Please ensure it is installed and in your PATH."
        ) from err
    except subprocess.CalledProcessError as err:
        print(f"LaTeX compilation stdout:\n{err.stdout}")
        print(f"LaTeX compilation stderr:\n{err.stderr}")
        raise RuntimeError(f"LaTeX compilation failed with exit code {err.returncode}") from err

    if not output_pdf.exists():
        raise RuntimeError(f"Expected output PDF '{output_pdf}' not found after compilation.")

    return output_pdf

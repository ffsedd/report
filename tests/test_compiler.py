import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from reptex.compiler import compile_latex  # replace your_module with actual module name

MINIMAL_LATEX = r"""
\documentclass{article}
\begin{document}
Hello, world!
\end{document}
"""


def test_compile_latex_creates_pdf(tmp_path: Path):
    output_pdf = tmp_path / "test.pdf"
    result = compile_latex(MINIMAL_LATEX, output_pdf, latexmk=False)
    assert result == output_pdf
    assert output_pdf.exists()
    # Optional: file size > 0
    assert output_pdf.stat().st_size > 0


def test_compile_latex_latexmk(tmp_path: Path):
    output_pdf = tmp_path / "test.pdf"
    result = compile_latex(MINIMAL_LATEX, output_pdf, latexmk=True)
    assert result == output_pdf
    assert output_pdf.exists()


@patch("subprocess.run", side_effect=FileNotFoundError())
def test_compile_latex_missing_executable(mock_run, tmp_path: Path):
    output_pdf = tmp_path / "test.pdf"
    with pytest.raises(OSError) as exc_info:
        compile_latex(MINIMAL_LATEX, output_pdf)
    assert "not found" in str(exc_info.value).lower()


@patch("subprocess.run")
def test_compile_latex_compilation_error(mock_run, tmp_path: Path):
    # Mock CalledProcessError with stdout/stderr attributes
    error = subprocess.CalledProcessError(
        returncode=1,
        cmd=["xelatex"],
        output="Some output",
        stderr="Error: missing something",
    )
    mock_run.side_effect = error

    output_pdf = tmp_path / "test.pdf"
    with pytest.raises(RuntimeError) as exc_info:
        compile_latex(MINIMAL_LATEX, output_pdf)
    assert "failed" in str(exc_info.value).lower()


@patch("subprocess.run")
def test_compile_latex_pdf_not_created(mock_run, tmp_path: Path):
    # mock successful run but no PDF created
    mock_run.return_value = MagicMock(returncode=0)

    output_pdf = tmp_path / "test.pdf"
    # Do NOT create the PDF file here to simulate missing output

    with pytest.raises(RuntimeError) as exc_info:
        compile_latex(MINIMAL_LATEX, output_pdf)
    assert "not found" in str(exc_info.value).lower()

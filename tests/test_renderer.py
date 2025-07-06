import shutil

import pytest

from reptex.compiler import compile_latex  # type: ignore

MINIMAL_LATEX = r"""
\documentclass{article}
\begin{document}
Hello, world!
\end{document}
"""


@pytest.fixture
def tmp_output_dir(tmp_path):
    # Provide a clean temporary directory for PDF output
    yield tmp_path


def test_compile_latex_basic(tmp_output_dir):
    output_pdf = tmp_output_dir / "output.pdf"
    pdf_path = compile_latex(MINIMAL_LATEX, output_pdf)

    # Check returned path matches output path
    assert pdf_path == output_pdf

    # Check PDF file exists and is non-empty
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0


@pytest.mark.skipif(
    shutil.which("latexmk") is None,
    reason="latexmk is not installed, skipping latexmk test",
)
def test_compile_latex_with_latexmk(tmp_output_dir):
    output_pdf = tmp_output_dir / "output_latexmk.pdf"
    pdf_path = compile_latex(MINIMAL_LATEX, output_pdf, latexmk=True)

    assert pdf_path == output_pdf
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0


@pytest.mark.skipif(
    shutil.which("xelatex") is None,
    reason="xelatex is not installed, skipping error handling test",
)
def test_compile_latex_bad_tex(tmp_output_dir):
    bad_tex = r"\documentclass{article}\begin{document}Missing end"
    output_pdf = tmp_output_dir / "bad_output.pdf"

    with pytest.raises(RuntimeError):
        compile_latex(bad_tex, output_pdf)

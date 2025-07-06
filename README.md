## reptex

**reptex** is a lightweight Python package for generating LaTeX reports programmatically.  
It renders report sections from Jinja2 templates and compiles them into a PDF using XeLaTeX or latexmk.

---

## Features

- Modular section-based report building
- Flexible Jinja2 template rendering with custom delimiters
- Compile LaTeX source directly to PDF
- Optional use of `latexmk` for multi-pass compilation

---

## Installation

```bash
git clone https://github.com/ffsedd/reptex.git
cd reptex
pip install -e .

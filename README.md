📄 RepTex - Modular Latex Report Generator

A lightweight and extensible Python tool for generating PDF reports using **Jinja2** templates and **LaTeX**. Built for automation, readability, and flexibility — suitable for technical reports, documentation, or scientific papers.

---

## ✨ Features

- 🧩 Template-based report structure (Jinja2 + LaTeX)
- 🧪 Type-safe configuration with Pydantic
- 📂 TOML-configured input/output paths
- 🧵 Modular codebase with pluggable sections
- 📦 Simple CLI interface

---

## 🛠️ Installation

Requires Python **3.10+**

```bash
uv pip install -e .



report/
├── src/
│   └── texreport/
│       ├── main.py              # CLI entry point
│       ├── config_loader.py     # Loads & validates TOML config using Pydantic
│       ├── template_renderer.py # Jinja2 + LaTeX engine
│       ├── sections.py          # Modular content blocks
│       └── latex_compiler.py    # PDF generation
├── src/report/config/
│   ├── report_config.toml       # Example report configuration
│   └── app_config.toml          # Optional global defaults
├── src/report/templates/
│   └── report_template.tex      # LaTeX Jinja2 template
├── .gitignore
├── pyproject.toml
└── README.md

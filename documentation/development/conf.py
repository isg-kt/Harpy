# Project Information
project: str = "Harpy"
copyright: str = "2026, Ismael Moreira"
author: str = "Ismael Moreira"
release: str = "0.1.0-alpha"

# Sphinx Configuration
extensions: list[str] = ["sphinx_copybutton", "sphinxcontrib.mermaid"]
templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

# Html Backend Configuration
html_theme: str = "alabaster"
html_static_path: list[str] = ["_static"]

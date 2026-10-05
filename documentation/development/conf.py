# Project Information
project: str = "Harpy"
copyright: str = "2026, Ismael Moreira"
author: str = "Ismael Moreira"
release: str = "0.1.0-alpha"

# Sphinx Configuration
extensions: list[str] = [
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
]
highlight_language: str = "text"
templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

# Html Backend Configuration
html_theme: str = "piccolo_theme"
html_title: str = "Harpy Programming Language"
html_static_path: list[str] = ["_static"]
html_css_files: list[str] = [
    "css/root.css",
    "css/links.css",
    "css/titles.css",
]
html_js_files: list[str] = []
# html_logo: str = "_static/images/logo.png"
html_favicon: str = "_static/images/favicon.ico"

"""Sphinx configuration file for the Harpy documentation.

Adds the local configuration directory to Python's path to import the
custom Harpy Pygments lexer, sets up project metadata, registers
extension modules, and configures the Piccolo HTML theme along with
custom CSS assets.
"""

import pathlib
import sys
import sphinx.application

sys.path.insert(0, str(pathlib.Path(__file__).parent / "configuration"))

import harpy_pigment

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


def setup(app: sphinx.application.Sphinx) -> dict[str, bool]:
    """Registers the custom Harpy Pygments lexer under the 'harpy' and
    'hrp' aliases.

    Returns extension metadata declaring compatibility with Sphinx
    parallel builds.
    """
    app.add_lexer("harpy", harpy_pigment.Lexer)
    app.add_lexer("hrp", harpy_pigment.Lexer)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

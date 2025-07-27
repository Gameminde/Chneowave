# Configuration file for the Sphinx documentation builder.
# CHNeoWave v1.0.0 - Documentation API

import os
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------

# Ajouter le répertoire source au path Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

# -- Project information -----------------------------------------------------

project = 'CHNeoWave'
copyright = '2024, Laboratoire d\'Études Maritimes'
author = 'Laboratoire d\'Études Maritimes'
release = '1.0.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
]

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Autosummary configuration
autosummary_generate = True
autosummary_imported_members = True

# Napoleon configuration (pour Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'qt': ('https://doc.qt.io/qtforpython/', None),
}

# Templates path
templates_path = ['_templates']

# Language
language = 'fr'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_context = {
    "display_github": True,
    "github_user": "laboratoire-maritime",
    "github_repo": "chneowave",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# Custom sidebar
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{lmodern}
''',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',
    'printindex': '\\footnotesize\\raggedright\\printindex',
}

latex_documents = [
    ('index', 'CHNeoWave.tex', 'Documentation CHNeoWave',
     'Laboratoire d\'Études Maritimes', 'manual'),
]

# -- Options for manual page output ------------------------------------------

man_pages = [
    ('index', 'chneowave', 'Documentation CHNeoWave',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    ('index', 'CHNeoWave', 'Documentation CHNeoWave',
     author, 'CHNeoWave', 'Logiciel d\'acquisition et d\'analyse de données maritimes.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

todo_include_todos = True

# -- Options for coverage extension ------------------------------------------

coverage_ignore_modules = [
    'tests',
    'setup',
]

coverage_ignore_functions = [
    'test_.*',
    '__.*__',
]

# -- Custom configuration ----------------------------------------------------

# Fonction pour ignorer certains warnings
def setup(app):
    app.add_css_file('custom.css')
    
# Ignorer les warnings pour les modules non trouvés
suppress_warnings = ['image.nonlocal_uri']

# Configuration pour les modules mock (si nécessaire)
autodoc_mock_imports = [
    'PyQt6',
    'PySide6',
    'pyqtgraph',
    'reportlab',
]

# Configuration pour les docstrings manquantes
nitpicky = False
nitpick_ignore = [
    ('py:class', 'type'),
    ('py:class', 'object'),
]
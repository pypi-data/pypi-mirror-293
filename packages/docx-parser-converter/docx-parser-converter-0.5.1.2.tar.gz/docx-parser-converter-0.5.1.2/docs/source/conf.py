import os
import sys

on_rtd = os.environ.get('READTHEDOCS') == 'True'

if on_rtd:
    sys.path.insert(0, os.path.abspath('../..'))  # Adjust this path as needed
else:
    sys.path.insert(0, os.path.abspath('../../docx_parser_converter'))  # Local path adjustment


project = 'Docx Parser and Converter'
copyright = '2024, Omer Hayun'
author = 'Omer Hayun'
release = '0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': True
}
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'lib'))

import sphinx_click
import sphinx_rtd_theme
import sphinx_autodoc_typehints
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Risksense API Library'
copyright = '2022, Ivanti'
author = 'arockia,thahasina,burr'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autosummary","sphinx.ext.autodoc","sphinx.ext.autosectionlabel","sphinx.ext.mathjax","sphinx.ext.viewcode","sphinx.ext.napoleon","sphinx.ext.intersphinx","sphinx.ext.extlinks","sphinx.ext.todo","sphinx.ext.coverage","sphinx.ext.ifconfig","sphinx.ext.githubpages", "sphinx_click.ext","sphinx_autodoc_typehints"]

templates_path = ['_templates']
exclude_patterns = []
pygments_style = "monokai"

# -- Options for HTML  ---------------------------------------------
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    "display_version": False,
    "prev_next_buttons_location": "both",
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
html_logo = "risksense_logo.png"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True


# -- Options for todo ----------------------------------------------
todo_include_todos = True

# -- Options for napoleon ------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_keyword = True
napoleon_use_rtype = True

# -- Options for autosectionlabel ----------------------------------
autosectionlabel_prefix_document = True

# -- Options for sphinx_autodoc_typehints --------------------------
set_type_checking_flag = True
typehints_fully_qualified = True
always_document_param_types = True
typehints_document_rtype = True


# -- Options for sphinx.ext.autodoc --------------------------------
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__,__call__",
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "__weakref__,__str__,__repr__",
}
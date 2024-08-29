import datetime

project = 'send-to-squey'
copyright = f"{datetime.date.today().year}, Squeylab"
author = 'Squeylab'

html_baseurl = 'https://send-to-squey.doc.squeylab.com/'
html_theme = 'furo'
html_static_path = ['_static']
html_js_files = ["js/piwik.js"]
html_show_sphinx = True
html_show_sourcelink = False

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# path to module
import os
import sys
sys.path.insert(0, os.path.abspath('../src/squeylab'))
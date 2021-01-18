from setuptools import setup

"""
Usage:
    python setup.py py2app
"""


APP = ['main.py']
DATA_FILES = ['data']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'data/logo.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps','easysettings'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

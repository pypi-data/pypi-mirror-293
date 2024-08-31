import pathlib
from setuptools import setup, find_packages

ROOT = pathlib.Path(__file__).parent

VERSION = '1.11.0'
PACKAGE_NAME = 'PyReconstruct'
AUTHOR = 'Julian Falco & Michael Chirillo'
AUTHOR_EMAIL = 'julian.falco@utexas.edu'
URL = 'https://github.com/SynapseWeb/PyReconstruct'
LICENSE = 'GNU GLPv3'
DESCRIPTION = 'RECONSTRUCT in Python'

LONG_DESCRIPTION = (ROOT / "readme.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'PySide6==6.5.2',
      'opencv-python==4.7.0.68',
      'numpy==1.24.1',
      'scikit-image==0.23.2',
      'trimesh==3.18.1',
      'vedo==2023.4.7',
      'zarr==2.18.2',
      'lxml==5.2.2',
      'gitpython==3.1.43',
      'qdarkstyle==3.2.3'
]


SHELL_SCRIPTS = []  # define shell scripts to install

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    package_data={'PyReconstruct': ['assets/**/*', 'assets/welcome_series/.welcome/*']},
    scripts=SHELL_SCRIPTS,
    entry_points={
        'console_scripts': [
            'PyReconstruct=PyReconstruct.cli:main'
        ]
    }
)

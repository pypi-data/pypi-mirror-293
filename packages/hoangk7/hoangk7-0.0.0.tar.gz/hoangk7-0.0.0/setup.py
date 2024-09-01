from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.0'
DESCRIPTION = 'test upload by hoang'
LONG_DESCRIPTION = 'A package that test upload a library.'

# Setting up
setup(
    name="hoangk7",
    version=VERSION,
    author="Hoang lt",
    author_email="kodzhoang@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['hoangk7', 'hoang', 'hoanglt'],
    python_requires = ">=3.10"
)
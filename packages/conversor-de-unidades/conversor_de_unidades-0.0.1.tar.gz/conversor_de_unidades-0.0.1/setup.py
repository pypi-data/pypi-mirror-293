from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

PACKAGE = 'conversor_de_unidades'
NAME = PACKAGE
DESCRIPTION = 'Converte direntes unidades'
VERSION = '0.0.1'
AUTHOR = 'DavidSilveira80'
EMAIL = 'davidpsdeveloper80@gmail.com'
URL = 'https://github.com/DavidSilveira80/simple-package-template'
PYTHON_REQUIRES = '>=3.9'

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=page_description,
    long_description_content_type='text/markdown',
    url=URL,
    packages=find_packages(),
    install_requires=requirements,
    python_requires=PYTHON_REQUIRES,
)

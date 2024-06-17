''' setup.py
'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tabeloader',
    version='0.8',
    author='new-village',
    url='https://github.com/new-village/tabeloader',
    description='tabeloader is a python library to collect the list of Top 100 restaurants in Japan from Tabelog.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'Apache-2.0 license',
    install_requires=['requests', 'bs4'],
    packages=find_packages(),
    package_data={'': ['config/*.json']},
)
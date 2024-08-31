from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="publish_poetry_test",
    version="0.0.3",
    author="ORION",
    author_email="datacollection@liferaftinc.com",
    packages=find_packages(),
    install_requires=[
    ],
    description="Publish_Poetry",
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
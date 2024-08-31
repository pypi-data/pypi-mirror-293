from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="Pipify_Components_Package",
    version="0.0.1",
    author="ORION",
    author_email="datacollection@liferaftinc.com",
    packages=find_packages(),
    install_requires=[
        'pika',
    ],
    description="Pipify_Components_Package",
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
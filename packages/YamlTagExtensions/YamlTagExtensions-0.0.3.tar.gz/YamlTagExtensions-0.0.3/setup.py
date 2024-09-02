from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='YamlTagExtensions',
    version='0.0.3',
    url='https://github.com/nayak-swastik/yaml-tag-extensions',
    description='Project with extended YAML functionality.',
    author='Swastik.Nayak',
    author_email='swastik.nayak.eu@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyYAML >= 6.0.2',
        'smart-open >= 7.0.4',
        'jinja2 >= 3.1.4'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

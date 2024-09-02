from setuptools import setup, find_packages

setup(
    name='YamlTagExtensions',
    version='0.0.1',
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
    long_description="Alpha version - Internal release."
)

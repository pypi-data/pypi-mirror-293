from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='pijoris',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts":[
            "pijoris-hello = pijoris:hello",
        ],
    },
    long_description=description,
    long_description_content_type='text/markdown'
)

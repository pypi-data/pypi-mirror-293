from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='pptesting',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    entry_points={
        "console_scripts": [
            "thisCanBeAnyName = pptesting:helloWorld",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
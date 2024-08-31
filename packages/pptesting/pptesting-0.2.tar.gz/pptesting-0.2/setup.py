from setuptools import setup, find_packages

setup(
    name='pptesting',
    version='0.2',
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
)
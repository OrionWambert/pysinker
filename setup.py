import setuptools

"""
Setup script for pysinker
to install the package run `pip install .`
"""
setuptools.setup(
    name="pysinker",
    version="0.1.0",
    description="",
    author="Orion WAMBERT",
    author_email="wambert.orion@gmail.com",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "pysinker=pysinker.main:app",
        ],
    },
    install_requires=[
        "typer",
        "setuptools",
        "pyyaml",
        "schedule",
    ],
)
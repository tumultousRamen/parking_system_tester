from setuptools import setup, find_packages

setup(
    name="parking-station",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
        "pytest-html>=4.1.1",
        "pytest-xdist>=3.3.1",
        "pytest-mock>=3.12.0",
    ],
)
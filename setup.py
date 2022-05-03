from setuptools import setup, find_packages

setup(
    name='facturio',
    version='1.0',
    packages=find_packages(),
    install_requires=["pygobject", "borb", "geopy"]
)

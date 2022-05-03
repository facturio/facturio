from setuptools import setup, find_packages

setup(
    name='facturio',
    description='un logiciel de gestion de factures.',
    version='1.0',
    url='https://github.com/facturio/facturio',
    packages=find_packages(),
    install_requires=["pygobject", "borb", "geopy"],
    entry_points={
        'console_scripts': [
            'facturio = facturio.main:main'
        ]
    },
)

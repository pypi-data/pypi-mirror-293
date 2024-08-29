from setuptools import setup

setup(
    name="odoo_endpoints",
    version='0.1.1',
    description='A package to unify odoo endpoints responses templates',
    url='https://github.com/MED-B/odoo_endpoint.git',

    author='MED-B',
    author_email='mohmed.khellaf@gmail.com',
    license='BSD 2-clause',
    #packages=[],
    install_requires=['odoo'],

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
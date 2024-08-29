# coding: utf-8
from setuptools import setup, find_packages


with open('requirements.txt', 'r') as req:
    requirements = [
        line.strip()
        for line in req
        if line.strip() and not line.strip().startswith('#')
    ]

setup(
    name='edutesting',
    description='Общая кодовая база для автотестов',
    version='0.7.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    include_package_data=True,
    url='https://stash.bars-open.ru/projects/EDUBASE/repos/edutesting',
    author='BARS Group',
    entry_points={
        'console_scripts': [
            "bparallel = edutesting.bparallel.__main__:main",
            "datatransfer = edutesting.mocks.datatransfer_server:main",
        ]
    }
)

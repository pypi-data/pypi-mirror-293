from setuptools import setup

setup(
    name='playgolf',
    version='0.3',
    packages=['playgolf'],
    package_data={'playgolf': ['data/*.csv']},
    include_package_data=True,
    install_requires=['pandas'],
    author='Raghul',
    author_email='raghulares@gmail.com',
    description='a package for S algorithm implementation with datasets included'
)
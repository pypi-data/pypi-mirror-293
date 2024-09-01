from setuptools import setup
from setuptools import find_packages
setup(
    name='playgolf',
    version='0.8',
    packages=find_packages(),
    package_data={'': ['playgolf_data.csv', 'playgolf_test.csv']},
    include_package_data=True,
    install_requires=['pandas'],
    author='Raghul',
    author_email='raghulares@gmail.com',
    description='a package for S algorithm implementation with datasets included'
)
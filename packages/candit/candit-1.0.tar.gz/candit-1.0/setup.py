from setuptools import setup, find_packages

setup(
    name='candit',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['enjoysport.csv']},
    install_requires=['numpy', 'pandas'],
    author='Raghul',
    author_email='raghulares@gmail.com'
)
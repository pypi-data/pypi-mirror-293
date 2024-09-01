from setuptools import setup, find_packages

setup(
    name='salgo',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['data.csv']},
    install_requires=[
        'pandas',
        'numpy',
    ],
    author='Raghul',
    author_email='raghulares@gmail.com',
    description='A package for S algorithm implementation with datasets included.'
)
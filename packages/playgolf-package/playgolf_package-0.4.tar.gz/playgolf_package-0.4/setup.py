from setuptools import setup, find_packages

setup(
    name='playgolf_package',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'playgolf_package': ['playgolf_data.csv', 'playgolf_test.csv'],
    },
    install_requires=[
        'pandas',
    ],
    description='A package for decision tree implementation with datasets included',
)

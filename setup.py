from setuptools import setup, find_packages

setup(
    name="companies_union",
    packages=find_packages(exclude=("test", "integration_test")),
    install_requires=['PyContracts', 'pandas', 'numpy', 'xlrd', 'openpyxl', 'cleanco', 'pytest']
)

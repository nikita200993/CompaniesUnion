from setuptools import setup, find_packages

setup(
    name="companies_union",
    packages=find_packages(),
    install_requires=['PyContracts', 'pandas', 'numpy', 'xlrd', 'openpyxl', 'cleanco', 'pytest']
)

from setuptools import setup, find_packages

setup(
    name='jadiss-finance-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
)
